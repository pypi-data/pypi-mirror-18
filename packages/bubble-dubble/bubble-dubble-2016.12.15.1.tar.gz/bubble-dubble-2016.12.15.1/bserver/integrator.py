#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import traceback
import threading
import platform
import numpy as np
from scipy.misc import imresize
from decor import floodfield, darkcurrent, distortion, background
from integracio import igracio
from ..bcommon import corrections, compressor


class Integrator:
    def __init__(self):
        self._lock = threading.Lock()
        self._i = igracio.IGracio()
        self.normalize = corrections.normalization.Normalization()
        self.mask = corrections.mask.Mask()
        self.background = background.Background()
        self.darkSample = darkcurrent.DarkCurrent()
        self.darkBackground = darkcurrent.DarkCurrent()
        self.flatfield = floodfield.FloodField()
        self.distortion = distortion.Distortion()

    def adjustCorrections(self, interface):
        self.interface = interface
        self._i.poni = self.interface.poni
        self._i.units = self.interface.units
        if self.interface.detector == 'Frelon':
            self.darkSample.init(self.interface.darkSample)
            self.darkBackground.init(self.interface.darkBackground)
            self.flatfield.init(self.interface.flood)
            self.distortion.init(self.interface.spline)
        else:
            self.darkSample.init(None)
            self.darkBackground.init(None)
            self.flatfield.init(None)
            self.distortion.init(None)
        self.normalize.beamline = self.interface.beamline
        self.mask.init(self.interface.maskFile, self.interface.beamline, self.interface.type)
        self.background.init(self.interface.backgroundFiles, self.darkBackground, self.normalize,
                             self.interface.bkgCoef, self.flatfield)

    def __call__(self, filename, image, interface, catchException=True):
        self.adjustCorrections(interface)
        if catchException:
            # noinspection PyBroadException
            try:
                result = self._integrate(filename, image)
            except:
                traceback.print_exc(file=sys.stdout)
                print('Frame: {}'.format(filename))
                return None
            else:
                return result
        else:
            return self._integrate(filename, image)

    def _integrate(self, filename, frames):
        retval = None
        ext = self.interface.ext
        if ext.startswith('.'):
            ext = ext[1:]
        if frames.header.get('Bubble_normalized', 0):
            return retval
        path, base = os.path.split(filename)
        newpath = os.path.join(path, self.interface.subdir)
        if frames.multiframe:
            newpath = os.path.join(newpath, base[:-4])
        try:  # it seems that here we can have race conditions
            os.makedirs(newpath)
        except OSError:
            pass
        for i, image in enumerate(frames):
            image = self.apply_corrections(image)
            res, chi = self._do_integration(image, base, newpath, ext, i)
            self.saveNormalizedFrame(chi, image)
            img, data = self.pack_data(image, res)
            if self.interface.sspeed:
                with self._lock:
                    self.interface.speedcounter += 1
            retval = {
                'imageFile': filename,
                'chiFile': chi,
                'transmission': image.transmission_coefficient,
                'data1d': data,
                'image': img,
                'timestamp': time.time(),
                'sent': False,
            }
        return retval

    def apply_corrections(self, image):
        image.float()
        image = self.darkSample(image)
        image = self.flatfield(image)
        image = self.normalize(image)
        image = self.background(image, self.interface.calcTransmission, self.interface.thickness,
                                self.interface.concentration)
        image.array *= self.interface.calibration
        image = self.mask(image)
        image.array = self.distortion(image.array)
        return image

    def pack_data(self, image, res):
        if self.interface.speed:
            image = None
        else:
            image = corrections.beamline.correctImage(self.interface.beamline, self.interface.type, image.array)
            if platform.system() != 'Linux':
                # on windows select.select is very inefficient, thus we downsample the image to 40%
                image = imresize(image, 40)
        if not self.interface.pickle:
            if image is not None:
                image = compressor.compressNumpyArray(image)
            res = [compressor.compressNumpyArray(array) for array in res]
        return image, res

    def _do_integration(self, image, base, newpath, ext, i):
        res, chi = None, None
        ext = ext if ext else 'dat'
        mf = '_{:05d}'.format(i) if image.multiframe else ''
        self._i.radial = self.interface.radial
        if self.interface.azimuthChecked and self.interface.azimuthSlices:
            step = self.interface.azimuth[0]
            for aslice in np.arange(0, 360, step):
                azmin, azmax = aslice, aslice + step
                res = self._i(image.array, azmin, azmax)
                chi = '{}{}_{:03.0f}_{:03.0f}.{}'.format(base[:-4], mf, azmin, azmax, ext)
                self._save_results(newpath, chi, res, image.transmission_coefficient)
        else:
            self._i.azimuth = self.interface.azimuth if self.interface.azimuthChecked else None
            res = self._i(image.array)
            chi = '{}{}.{}'.format(base[:-4], mf, ext)
            self._save_results(newpath, chi, res, image.transmission_coefficient)
        return res, chi

    def _save_results(self, newpath, chi, res, transCoef):
        chi = os.path.join(newpath, chi)
        np.savetxt(chi, np.array(res).T, '%.6e')
        if self.interface.calcTransmission:
            with open(chi, 'r+') as fchi:
                old = fchi.read()
                fchi.seek(0)
                fchi.write('# Transmission coefficient {0:.7f}\n{1}'.format(transCoef, old))

    def saveNormalizedFrame(self, chifile, image):
        if self.interface.save:
            image.array = image.array.astype(np.int32)
            name = '{}_norm.edf'.format(chifile[:-4])
            image.save_edf(name, Bubble_normalized=1)
