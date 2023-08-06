#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import _cryio


class CCP4Image(_cryio._ccp4_encode):
    def save(self, filename):
        with open(filename, 'wb') as f:
            f.write(bytes(self))
