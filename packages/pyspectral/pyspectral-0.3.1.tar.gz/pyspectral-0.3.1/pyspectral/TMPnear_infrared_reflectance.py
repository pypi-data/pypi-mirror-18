#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, 2015 Adam.Dybbroe

# Author(s):

#   Adam.Dybbroe <adam.dybbroe@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Derive the Near-Infrared reflectance of a given band in the solar and
thermal range (usually the 3.7-3.9 micron band) using a thermal atmospheric
window channel (usually around 11-12 microns).
"""
import logging
LOG = logging.getLogger(__name__)

import ConfigParser
import os

CONFIG_FILE = os.environ.get('PSP_CONFIG_FILE', None)
if CONFIG_FILE and (not os.path.exists(CONFIG_FILE) or not os.path.isfile(CONFIG_FILE)):
    raise IOError(str(CONFIG_FILE) + " pointed to by the environment " +
                  "variable PSP_CONFIG_FILE is not a file or does not exist!")
elif not CONFIG_FILE:
    LOG.warning('Environment variable PSP_CONFIG_FILE not set!')

import numpy as np
from pyspectral.solar import (SolarIrradianceSpectrum,
                              TOTAL_IRRADIANCE_SPECTRUM_2000ASTM)
from pyspectral.utils import BANDNAMES

WAVE_LENGTH = 'wavelength'
WAVE_NUMBER = 'wavenumber'

EPSILON = 0.01
TB_MIN = 150.
TB_MAX = 360.

SATNAME = {'eos1': 'terra',
           'eos2': 'aqua'}

from pyspectral.radiance_tb_conversion import RadTbConverter


class Calculator(RadTbConverter):

    """A thermal near-infrared (e.g. 3.7 micron) band reflectance calculator.

    Given the relative spectral response of the NIR band, the solar zenith
    angle, and the brightness temperatures of the NIR and the Thermal bands,
    derive the solar reflectance for the NIR band removing the thermal
    (terrestrial) part.  The in-band solar flux over the NIR band is
    optional. If not provided, it will be calculated here!

    The relfectance calculated is without units and should be between 0 and 1.
    """

    def __init__(self, platform, satnum, instrument, bandname,
                 solar_flux=None, **options):
        super(Calculator, self).__init__(platform, satnum, instrument,
                                         bandname, method=1, **options)

        self.bandname = BANDNAMES.get(bandname, bandname)

        if CONFIG_FILE:
            conf = ConfigParser.ConfigParser()
            try:
                conf.read(CONFIG_FILE)
            except ConfigParser.NoSectionError:
                LOG.warning(
                    'Failed reading configuration file: ' + str(CONFIG_FILE))

            satellite = platform + satnum
            options = {}
            for option, value in conf.items(SATNAME.get(satellite, satellite) +
                                            '-' + instrument,
                                            raw=True):
                options[option] = value

        if solar_flux is None:
            self._get_solarflux()
        else:
            self.solar_flux = solar_flux
        self._rad37 = None
        self._rad37_t11 = None
        self._solar_radiance = None
        self._rad39_correction = 1.0

        if 'detector' in options:
            self.detector = options['detector']
        else:
            self.detector = 'det-1'

        if self.instrument == 'seviri':
            self.ch37name = 'IR3.9'
        elif self.instrument == 'modis':
            self.ch37name = '20'
        elif self.instrument == 'ahi':
            self.ch37name = 'ch7'
        else:
            raise NotImplementedError('Not yet support for this ' +
                                      'instrument ' + str(self.instrument))

        resp = self.rsr[self.bandname][self.detector]['response']
        wv_ = self.rsr[self.bandname][self.detector][self.wavespace]
        self.rsr_integral = np.trapz(resp, wv_)

        if 'tb2rad_lut_filename' in options:
            self.lutfile = options['tb2rad_lut_filename']
            LOG.info("lut filename: " + str(self.lutfile))
            if not os.path.exists(self.lutfile):
                self.lut = self.make_tb2rad_lut(self.bandname,
                                                self.lutfile)
                LOG.info("LUT file created")
            else:
                self.lut = self.read_tb2rad_lut(self.lutfile)
                LOG.info("File was there and has been read!")
        else:
            LOG.info("No lut filename available in config file. " +
                     "No lut will be used")
            self.lutfile = None
            self.lut = None

        self._solar_part_only = None
        self._thermal_part_only = None

    def derive_rad39_corr(self, bt11, bt13, method='rosenfeld'):
        """Derive the 3.9 radiance correction factor to account for the
        attenuation of the emitted 3.9 radiance by CO2 absorption. Requires the
        11 micron window band and the 13.4 CO2 absorption band, as
        e.g. available on SEVIRI. Currently only supports the Rosenfeld method"""
        if method != 'rosenfeld':
            raise AttributeError("Only CO2 correction for SEVIRI using " +
                                 "the Rosenfeld equation is supported!")

        LOG.debug("Derive the 3.9 micron radiance CO2 correction coefficent")
        self._rad39_correction = (bt11 - 0.25 * (bt11 - bt13)) ** 4 / bt11 ** 4

    def _get_solarflux(self):
        """Derive the in-band solar flux from rsr over the Near IR band (3.7 or
        3.9 microns)"""
        solar_spectrum = SolarIrradianceSpectrum(TOTAL_IRRADIANCE_SPECTRUM_2000ASTM,
                                                 dlambda=0.0005,
                                                 wavespace=self.wavespace)
        self.solar_flux = solar_spectrum.inband_solarflux(
            self.rsr[self.bandname])

    def reflectance_from_tbs(self, sun_zenith, tb_near_ir, tb_thermal,
                             tb_ir_co2=None):
        """
        The relfectance calculated is without units and should be between 0 and
        1.
        Inputs:

          sun_zenith: Sun zenith angle for every pixel - in degrees

          tb_near_ir: The 3.7 (or 3.9 or equivalent) IR Tb's at every pixel
                      (Kelvin)

          tb_thermal: The 10.8 (or 11 or 12 or equivalent) IR Tb's at every
                      pixel (Kelvin)

          tb_ir_co2: The 13.4 micron channel (or similar - co2 absorption band)
                     brightness temperatures at every pixel. If None, no CO2
                     absorption correction will be applied.

        """

        if np.isscalar(tb_near_ir):
            tb_nir = np.array([tb_near_ir, ])
        else:
            tb_nir = np.array(tb_near_ir)

        if np.isscalar(tb_thermal):
            tb_therm = np.array([tb_thermal, ])
        else:
            tb_therm = np.array(tb_thermal)

        if tb_therm.shape != tb_nir.shape:
            raise ValueError('Dimensions does not match!' +
                             str(tb_therm.shape) + ' and ' + str(tb_nir.shape))

        if tb_ir_co2 is None:
            co2corr = False
            tbco2 = None
        else:
            co2corr = True
            if np.isscalar(tb_ir_co2):
                tbco2 = np.array([tb_ir_co2, ])
            else:
                tbco2 = np.array(tb_ir_co2)

        if self.instrument == 'seviri':
            ch37name = 'IR3.9'
        elif self.instrument == 'modis':
            ch37name = '20'
        else:
            raise NotImplementedError('Not yet support for this ' +
                                      'instrument ' + str(self.instrument))

        if not self.rsr:
            raise NotImplementedError("Reflectance calculations without " +
                                      "rsr not yet supported!")
            # retv = self.tb2radiance_simple(tb_therm, self.ch37name)
            # print("tb2radiance_simple conversion: " + str(retv))
            # thermal_emiss_one = retv['radiance']
            # retv = self.tb2radiance_simple(tb_nir, self.ch37name)
            # print("tb2radiance_simple conversion: " + str(retv))
            # l_nir = retv['radiance']
        else:
            # Assume rsr in in microns!!!
            # FIXME!
            scale = self.rsr_integral * 1e-6
            retv = self.tb2radiance(tb_therm, self.ch37name, self.lut)
            # print("tb2radiance conversion: " + str(retv))
            thermal_emiss_one = retv['radiance'] * scale
            retv = self.tb2radiance(tb_nir, self.ch37name, self.lut)
            # print("tb2radiance conversion: " + str(retv))
            l_nir = retv['radiance'] * scale

        if thermal_emiss_one.ravel().shape[0] < 10:
            LOG.info('thermal_emiss_one = ' + str(thermal_emiss_one))
        if l_nir.ravel().shape[0] < 10:
            LOG.info('l_nir = ' + str(l_nir))

        sunz = np.ma.masked_outside(sun_zenith, 0.0, 88.0)
        sunzmask = sunz.mask
        sunz = sunz.filled(88.)

        mu0 = np.cos(np.deg2rad(sunz))
        # mu0 = np.where(np.less(mu0, 0.1), 0.1, mu0)
        self._rad37 = l_nir
        self._rad37_t11 = thermal_emiss_one
        self._solar_radiance = 1. / np.pi * self.solar_flux * mu0

        # CO2 correction to the 3.9 radiance, only if tbs of a co2 band around
        # 13.4 micron is provided:
        if co2corr:
            self.derive_rad39_corr(tb_therm, tbco2)

        self._thermal_part_only = thermal_emiss_one * self._rad39_correction
        self._solar_part_only = l_nir

        nomin = self._solar_part_only - self._thermal_part_only
        LOG.debug("Shapes: " + str(mu0.shape) + "  " +
                  str(thermal_emiss_one.shape))
        denom = self._solar_radiance - self._thermal_part_only

        r39 = nomin / denom
        r39 = np.ma.masked_where(sunzmask, r39)

        # Reflectances should be between 0 and 1, but values above 1 is
        # perfectly possible and okay! (Multiply by 100 to get reflectances
        # in percent)
        return r39

    def get_solar_part(self, radiance=True):
        """Get only the solar contribution to the observed radiance"""

        if radiance:
            return self._solar_part_only
        else:
            return self.radiance2tb(radiance, self.ch37name, self.lut)
