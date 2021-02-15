"""
어떤 방식으로 제작할것인가.
1. 자막 파일을 연다 들인다.
2. 자막 파일에서 1줄씩 읽어 들이며 정규표현식에 해당하는 부분을 추출해낸다 (그륩)
3. 추출해낸 부분에 정의한 첫 딜레이만큼 줄이거나 늘인다.
4. 폴더 위치를 지정하여 해당하는 자막 파일들을 지정하여 전부 동일하게 적용한다.
"""

import datetime
import re
import os
import shutil

log_folder_name = "pre_log"


def file_open_utf(file_name):
    try:
        f = open(file_name, "r+", encoding="UTF-8")
        pre_tell = f.tell()
        read_data = f.readline()

    except UnicodeDecodeError:
        # UTF-16-le 사용시 tell및 seek에서 BOM 에러가 발생하지 않는다.
        f = open(file_name, "r+", encoding="UTF-16-le")
        pre_tell = f.tell()
        read_data = f.readline()

    return f, pre_tell, read_data


def sync_ass(file_name, delay):
    f, pre_tell, read_data = file_open_utf(file_name)
    while read_data:
        p = re.compile(r'(Dialogue: 0,)(\d:\d{2}:\d{2}.\d{2})(,)(\d:\d{2}:\d{2}.\d{2})(.+)')
        m = p.match(read_data)
        try:
            change_str = []
            for i in range(2, 5, 2):
                dt_time = datetime.datetime.strptime(m.group(i), r"%H:%M:%S.%f")
                sec_delay, mic_delay = divmod(delay, 1000)
                td_delay = datetime.timedelta(seconds=sec_delay,
                                              microseconds=mic_delay * 1000 % 1000000)
                td = dt_time + td_delay
                change_str.append(td.strftime(r"%H:%M:%S.%f")[1:-4])

            change_data = []
            iter_data = iter(change_str)
            for i, insert_data in enumerate(m.groups()):
                if i == 1 or i == 3:
                    change_data.append(next(iter_data))
                else:
                    change_data.append(insert_data)

            result_str = ''.join(change_data)
            f.seek(pre_tell, 0)
            f.write(result_str)

        except AttributeError:
            pass

        pre_tell = f.tell()
        read_data = f.readline()
    f.close()


def sync_smi(file_name, delay):
    f, pre_tell, read_data = file_open_utf(file_name)
    while read_data:
        p = re.compile(r'(<Sync Start=)(\d+)(.+)')
        m = p.match(read_data)
        try:
            file_time = int(m.group(2))
            change_time = file_time + delay

            change_data = []
            for i, insert_data in enumerate(m.groups()):
                if i == 1:
                    change_data.append(change_time)
                else:
                    change_data.append(insert_data)

            result_str = ''.join(map(str, change_data))
            f.seek(pre_tell, 0)
            f.write(result_str)

        except AttributeError:
            pass

        pre_tell = f.tell()
        read_data = f.readline()
    f.close()


def select_file_ext(file, delay, ext):
    if ext == ".ass":
        sync_ass(file, delay)
    elif ext == ".smi":
        sync_smi(file, delay)


def main_cc(file, delay, logstat, time_start=None, time_end=None):
    if logstat and (not os.path.exists(log_folder_name)):
        os.mkdir(log_folder_name)

    if os.path.isfile(file):
        _, ext = os.path.splitext(file)

        if ext == ".ass" or ext == ".smi":
            if logstat:
                log_file = os.path.join(log_folder_name, file)
                if not os.path.exists(log_file):
                    shutil.copy2(file, log_file)
                    select_file_ext(file, delay, ext)
                else:
                    print("이미 존재하는 로그 파일입니다. \n덮어 쓰시겠습니까?")
            else:
                select_file_ext(file, delay, ext)
