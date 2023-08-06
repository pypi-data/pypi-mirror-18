import unittest

from datetime import datetime
from tenkishocho import DayPerMonthTenki

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

    def test_ret_predicted_outer_data_list_with_kishocho(self):
        target_date = datetime(2015, 12, 24).date()
        dpmt = DayPerMonthTenki(target_date.year, target_date.month)

        # Test _ret_temp_max_with_dpmt function
        temp_max = utils._ret_temp_max_with_dpmt(dpmt, target_date)
        self.assertEqual(temp_max, 15.4)

        # Test _ret_temp_min_with_dpmt function
        temp_min = utils._ret_temp_min_with_dpmt(dpmt, target_date)
        self.assertEqual(temp_min, 5.5)

        # Test _ret_humidity_ave_with_dpmt function
        humidity_ave = utils._ret_humidity_ave_with_dpmt(dpmt, target_date)
        self.assertEqual(humidity_ave, 82.0)

        # Test _ret_tenki_with_dpmt function
        tenki = utils._ret_tenki_with_dpmt(dpmt, target_date)
        self.assertEqual(tenki, 0.0)

        # Test ret_predicted_outer_data_list_with_kishocho
        pod_list = utils.ret_predicted_outer_data_list_with_kishocho(target_date)
        self.assertEqual(pod_list, [0.0, 15.4, 5.5, 82.0, 0.0])  # 2015-12-24 is Thurseday
