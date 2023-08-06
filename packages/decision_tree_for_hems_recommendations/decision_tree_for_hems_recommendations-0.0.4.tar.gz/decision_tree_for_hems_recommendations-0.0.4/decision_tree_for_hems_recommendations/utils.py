import os
from datetime import datetime as dt
from datetime import timedelta as delta

import numpy as np
from sklearn.tree.tree import DecisionTreeClassifier

import pyowm

from tenkishocho import DayPerMonthTenki


def ret_OWM_API_KEY():
    api = os.getenv('OWM_API_KEY')
    if not api:
        raise Exception('OWM_API_KEY not found')
    return api

def is_rain_or_not(char):
    '''
    >>> is_rain_or_not('晴時々曇')
    0.0
    >>> is_rain_or_not('曇一時雨')
    1.0
    '''
    if '雨' in char:
        return 1.0
    elif 'みぞれ' in char:
        return 1.0
    elif '雪' in char:
        return 1.0
    return 0.0


def _ret_dpmt_list(start_dt, end_dt):
    dpmt_list = []
    # get targeted year list order by year num
    targeted_year_list = [y for y in range(start_dt.year, end_dt.year + 1)]
    stat_dt = start_dt
    while stat_dt.year < end_dt.year or stat_dt.month <= end_dt.month:
        dpmt_list.append(DayPerMonthTenki(stat_dt.year, stat_dt.month))
        if stat_dt.month in (1, 3, 5, 7, 8, 10, 12):
            stat_dt += delta(days=31)
        else:
            stat_dt += delta(days=30)
    return dpmt_list


def _ret_date_list(start_dt, end_dt):
    stat_dt = start_dt
    date_list = []
    while stat_dt <= end_dt:
        # 日付リスト作成
        date_list.append(stat_dt.date())
        stat_dt += delta(days=1)
    return date_list

def _ret_weekday_list(start_dt, end_dt):
    stat_dt = start_dt
    weekday_list = []
    while stat_dt <= end_dt:
        # 平日休日リスト作成
        # 平日:'w' or 0.0, 休日:'h' or 1.0
        wd = stat_dt.weekday()  # 曜日取得
        if 0 <= wd <= 4:
            # weekday_list.append('w')
            weekday_list.append(0.0)
        elif 5 <= wd <= 6:
            # weekday_list.append('h')
            weekday_list.append(1.0)
        stat_dt += delta(days=1)
    return weekday_list


def _ret_outer_env_list(start_dt, end_dt):
    # tenkishocho DayPerMonthTenki オブジェクトを取得
    dpmt_list = _ret_dpmt_list(start_dt, end_dt)

    max_temperature_list = []
    min_temperature_list = []
    ave_humidity_list = []
    day_tenki_list = []
    for index, dpmt in enumerate(dpmt_list):
        if index == 0:
            first_month_flag = True
        else:
            first_month_flag = False

        if index == len(dpmt_list) - 1:
            end_month_flag = True
        else:
            end_month_flag = False

        # 最高気温
        for day, v in dpmt.get_max_temperature().items():
            if first_month_flag and day < start_dt.day:
                continue
            if end_month_flag and day > end_dt.day:
                break
            max_temperature_list.append(v)

        # 最低気温
        for day, v in dpmt.get_min_temperature().items():
            if first_month_flag and day < start_dt.day:
                continue
            if end_month_flag and day > end_dt.day:
                break
            min_temperature_list.append(v)

        # 平均湿度
        for day, v in dpmt.get_ave_humidity().items():
            if first_month_flag and day < start_dt.day:
                continue
            if end_month_flag and day > end_dt.day:
                break
            ave_humidity_list.append(v)

        # 日中天候
        for day, v in dpmt.get_day_tenki().items():
            if first_month_flag and day < start_dt.day:
                continue
            if end_month_flag and day > end_dt.day:
                break
            day_tenki_list.append(is_rain_or_not(v))

    return (max_temperature_list, min_temperature_list,
            ave_humidity_list, day_tenki_list)


def ret_outer_data_list(start_dt, end_dt):
    '''
    Tenki data

    example list to make
    [
        [datetime(2016, 7, 1) 1.0, 31.0, 25.0, 77.2, 0.0],
        [datetime(2016, 7, 2) 1.0, 29.8, 24.8, 70.2, 0.0],
        .
        .
        .
        [datetime(2016, 8, 15) 1.0, 31, 25, 73.2, 0.0],
    ]
    date_list, weekday_list, max_temperature_list, min_temperature_list, ave_humidity_list, day_tenki_list

    [[datetime.date(2016, 7, 31), 1.0, 30.8, 24.4, 60.0, 1.0], [datetime.date(2016, 8, 1), 0.0, 31.5, 24.6, 60.0, 1.0]]
    '''

    # get date_list
    date_list = _ret_date_list(start_dt, end_dt)
    # get weekday_list
    weekday_list = _ret_weekday_list(start_dt, end_dt)
    # get env_lists
    max_temperature_list, min_temperature_list, \
        ave_humidity_list, day_tenki_list = _ret_outer_env_list(
            start_dt, end_dt
        )

    # check the lists length
    if len(date_list) != len(max_temperature_list):
        raise Exception('これからzipしていくリストの長さが違うでよ')

    ret_list = [[c1, c2, c3, c4, c5, c6] for c1, c2, c3, c4, c5, c6 in zip(
        date_list,
        weekday_list,
        max_temperature_list,
        min_temperature_list,
        ave_humidity_list,
        day_tenki_list
    )]

    return ret_list


def ret_date_list(start_dt, end_dt):
    stat_dt = start_dt
    ret_list = []
    while stat_dt <= end_dt:
        # 日付リスト作成
        ret_list.append(stat_dt.date())
        stat_dt += delta(days=1)
    return ret_list


def be_ndarray(x):
    return np.array(x)


def ret_trained_DT_clf(X, Y):
    clf = DecisionTreeClassifier(max_depth=3)
    clf.fit(X, Y)
    return clf


def ret_predicted_outer_data_list_with_OWM(OWM_API_KEY, target_date=dt.now().date()):
    '''
    Tenki data

    example list to make
    [1.0, 31.0, 25.0, 77.2, 0.0],
    weekday_list, max_temperature_list, min_temperature_list, ave_humidity_list, day_tenki_list
    '''

    # 平日休日 weekday
    wd = target_date.weekday()  # 曜日取得
    # 平日=>0.0, 休日=>1.0
    weekday = 0.0 if 0 <= wd <= 4 else 1.0

    # Instanciate owm and weather
    owm = pyowm.OWM(OWM_API_KEY)
    observation = owm.weather_at_place('Tokoyo,jp')
    weather = observation.get_weather()

    # 最大気温 temp_max
    temp_max = weather.get_temperature('celsius')['temp_max']

    # 最低気温 temp_min
    temp_min = weather.get_temperature('celsius')['temp_min']

    # 平均湿度 humidity_ave
    humidity_ave = weather.get_humidity()

    # 日中天候 tenki
    w_icon = weather.get_weather_icon_name()
    sunnuy_icon_tupple = (
        '01d', '01n',
        '02d', '02n',
        '03d', '03n',
        '04d', '04n',
    )
    rainy_icon_tupple = (
        '09d', '09n',
        '10d', '10n',
        '11d', '11n',
        '12d', '12n',
        '13d', '13n',
        '50d', '50n',
    )
    tenki = 0.0 if w_icon in sunnuy_icon_tupple else 1.0

    # make ret_list
    ret_list = [weekday, temp_max, temp_min, humidity_ave, tenki]

    return ret_list


def _ret_temp_max_with_dpmt(dpmt, target_date):
    temp_max = [v for day, v in dpmt.get_max_temperature().items() \
        if day == target_date.day][0]
    return temp_max


def _ret_temp_min_with_dpmt(dpmt, target_date):
    temp_min = [v for day, v in dpmt.get_min_temperature().items() \
        if day == target_date.day][0]
    return temp_min


def _ret_humidity_ave_with_dpmt(dpmt, target_date):
    humidity_ave = [v for day, v in dpmt.get_ave_humidity().items() \
        if day == target_date.day][0]
    return humidity_ave


def _ret_tenki_with_dpmt(dpmt, target_date):
    '''
    雨でないとき->0.0
    雨のとき->1.0
    を返す
    '''
    tenki_str = [v for day, v in dpmt.get_day_tenki().items() \
        if day == target_date.day][0]
    tenki = is_rain_or_not(tenki_str)
    return tenki


def ret_predicted_outer_data_list_with_kishocho(target_date):
    '''
    Tenki data

    example list to make
    [1.0, 31.0, 25.0, 77.2, 0.0],
    weekday_list, max_temperature_list, min_temperature_list, ave_humidity_list, day_tenki_list
    '''

    # 平日休日 weekday
    wd = target_date.weekday()  # 曜日取得
    # 平日=>0.0, 休日=>1.0
    weekday = 0.0 if 0 <= wd <= 4 else 1.0


    # get the target_date's DayPerMonthTenki instance
    dpmt = DayPerMonthTenki(target_date.year, target_date.month)

    temp_max = _ret_temp_max_with_dpmt(dpmt, target_date)
    temp_min = _ret_temp_min_with_dpmt(dpmt, target_date)
    humidity_ave = _ret_humidity_ave_with_dpmt(dpmt, target_date)
    # tenki
    tenki = _ret_tenki_with_dpmt(dpmt, target_date)

    # make ret_list
    ret_list = [weekday, temp_max, temp_min, humidity_ave, tenki]

    return ret_list

def make_delta_hour(start_dt, end_dt=dt.now()):
    """
    >>> start_dt = dt(2016, 4, 1, 10, 40, 0)
    >>> end_dt = dt(2016, 4, 1, 15, 40, 0)
    >>> make_delta_hour(start_dt, end_dt)
    5.0
    """
    delta_seconds = (end_dt - start_dt).seconds
    return round((delta_seconds // 60) / 60, 1)


def make_days_last_timestamp(the_time=dt.now()):
    return dt(the_time.year, the_time.month, the_time.day, 23, 59, 59)
