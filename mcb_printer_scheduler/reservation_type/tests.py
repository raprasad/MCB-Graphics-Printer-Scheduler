import unittest
from test_reservation_type import ReservationTypeTest

def suite():
    suite = unittest.TestSuite()
    #suite.addTest(TreeRearrangement('runTest'))
    #suite.addTest(NodeTestCase('test_root'))
    suite.addTest(ReservationTypeTest('runTest'))
    return suite        
