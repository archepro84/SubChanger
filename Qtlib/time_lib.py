from datetime import datetime, time, timedelta


def time_to_msec(time_data):
    timer = 0
    timer += time_data.microsecond / 1000
    timer += time_data.second * 1000
    timer += time_data.minute * (1000 * 60)
    timer += time_data.hour * (1000 * 60 * 60)
    return int(timer)


def msec_to_time(msec_data):
    hour_data, hour_temp = divmod(msec_data, (1000 * 60 * 60))
    min_data, min_temp = divmod(hour_temp, (1000 * 60))
    sec_data, msec = divmod(min_temp, 1000)
    data = time(hour=hour_data, minute=min_data, second=sec_data, microsecond=msec * 1000)
    return data


# time_data = time(hour=11, minute=22, second=33, microsecond=444000)
# time_data2 = time(hour=11, minute=22, second=33, microsecond=444000)
#
# result = time_to_msec(time_data)
# print(msec_to_time(result))
