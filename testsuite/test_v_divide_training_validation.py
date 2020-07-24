"""
Name:       v.divide.training_validation test
Purpose:    Tests v.divide.training_validation input parsing.
            Uses NC Basic data set.

Author:     Markus Neteler
Copyright:  (C) 2020 Markus Neteler, mundialis, and the GRASS Development Team
Licence:    This program is free software under the GNU General Public
            License (>=v2). Read the file COPYING that comes with GRASS
            for details.
"""

import os

from grass.gunittest.case import TestCase
from grass.gunittest.main import test

class Testdivide(TestCase):
    inpoint = 'landclass_points'
    outtrain = 'training'
    outvalid = 'validation'

    @classmethod
    def setUpClass(cls):
        """Ensures expected computational region and generated data"""
        cls.use_temp_region()
        # map with 21 points
        cls.runModule('v.unpack', input='landclass_points.pack')
        cls.runModule('g.region', vector=cls.inpoint)

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary region and generated data"""
#        cls.runModule('g.remove', flags='f', type='vector',
#                      name=(cls.outtrain, cls.outvalid))
        cls.del_temp_region()

    def test_points(self):
        """Test divide points"""
        self.assertModule('v.divide.training_validation', input=self.inpoint, column='landclass96',
                          training=self.outtrain, validation=self.outvalid, training_percent=33)
        self.assertVectorExists(self.outtrain)
        self.assertVectorExists(self.outvalid)
        topology = dict(points=7)
        self.assertVectorFitsTopoInfo(self.outtrain, topology)
        topology = dict(points=14)
        self.assertVectorFitsTopoInfo(self.outvalid, topology)

if __name__ == '__main__':
    test()
