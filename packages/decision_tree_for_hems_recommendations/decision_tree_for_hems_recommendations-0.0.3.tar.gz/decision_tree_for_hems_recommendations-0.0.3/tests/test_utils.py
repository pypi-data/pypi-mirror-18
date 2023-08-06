import unittest

from datetime import datetime


from decision_tree_for_hems_recommendations import utils


class UtilsTestCase(unittest.TestCase):
    def test__ret_dpmt_list(self):
        start_dt = datetime(2015, 12, 1)
        end_dt = datetime(2016, 1, 31)
        dlist = utils._ret_dpmt_list(
            start_dt=start_dt,
            end_dt=end_dt
        )
        # length check
        self.assertEqual(len(dlist), 2)

    def test__ret_date_list(self):
        start_dt = datetime(2015, 12, 1)
        end_dt = datetime(2016, 1, 31)
        dlist = utils._ret_date_list(
            start_dt=start_dt,
            end_dt=end_dt
        )
        # length check
        self.assertEqual(len(dlist), 62)

        self.assertEqual(dlist[0], datetime(2015, 12, 1).date())
        self.assertEqual(dlist[61], datetime(2016, 1, 31).date())

    def test__ret_weekday_list(self):
        start_dt = datetime(2015, 12, 1)
        end_dt = datetime(2016, 1, 31)
        dlist = utils._ret_weekday_list(
            start_dt=start_dt,
            end_dt=end_dt
        )
        # length check
        self.assertEqual(len(dlist), 62)

        self.assertEqual(dlist[0], 0.0)  # 2015-12-01 is Tuesday
        self.assertEqual(dlist[4], 1.0)  # 2015-12-05 is Saturday

    def test__ret_outer_env_list(self):
        start_dt = datetime(2015, 12, 1)
        end_dt = datetime(2016, 1, 31)
        dlist, dlist1, dlist2, dlist3 = utils._ret_outer_env_list(
            start_dt=start_dt,
            end_dt=end_dt
        )
        # length check
        self.assertEqual(len(dlist), 62)

    def test_ret_outer_data_list(self):
        start_dt = datetime(2015, 12, 1)
        end_dt = datetime(2016, 1, 31)
        dlist = utils.ret_outer_data_list(start_dt, end_dt)
        # length
        # length check
        self.assertEqual(len(dlist), 62)
