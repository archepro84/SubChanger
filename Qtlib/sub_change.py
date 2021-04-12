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
from myNote.SubChanger.Qtlib.time_lib import *

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


def sync_ass(file_name, delay, start_time=None, end_time=None):
    f, pre_tell, read_data = file_open_utf(file_name)
    while read_data:
        p = re.compile(r'(Dialogue: \d,)(\d:\d{2}:\d{2}.\d{2})(,)(\d:\d{2}:\d{2}.\d{2})(.+)')
        m = p.match(read_data)
        try:
            change_str = []
            # TODO 1번의 불필요한 변환이 존재함 수정이 필요.
            if start_time and end_time:
                if not (start_time <=
                        time_to_msec(datetime.datetime.strptime(m.group(2), r"%H:%M:%S.%f"))
                        <= end_time):
                    pre_tell = f.tell()
                    read_data = f.readline()
                    continue

            for i in range(2, 5, 2):
                dt_time = datetime.datetime.strptime(m.group(i), r"%H:%M:%S.%f")
                sec_delay, mic_delay = divmod(delay, 1000)
                td_delay = datetime.timedelta(seconds=sec_delay,
                                              microseconds=mic_delay * 1000 % 1000000)
                td = dt_time + td_delay
                change_str.append(td.strftime(r"%H:%M:%S.%f")[1:-4])

            change_data = []
            # TODO iter 형식의 반복문 수정
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


def sync_smi(file_name, delay, start_time=None, end_time=None):
    f, pre_tell, read_data = file_open_utf(file_name)
    while read_data:
        # TODO 대소문자 구분 없이 설정
        p = re.compile(r'(<SYNC Start=)(\d+)(.+)')
        # p = re.compile(r'(<Sync Start=)(\d+)(.+)')
        m = p.match(read_data)
        try:
            file_time = int(m.group(2))
            change_time = file_time + delay
            if change_time < 0:
                change_time = 0


            if start_time and end_time:
                if not (start_time <= file_time <= end_time):
                    # TODO smi의 end_time 이후 &nbsp;만이 단독으로 delay되지 않는다면? (자막이 지워지지 않고 연속 출력되는현상 발생)
                    # 부분수정으로인한 자막의 오류발생은 어떻게 처리해야하는가?
                    change_time = file_time

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


# TODO Log 저장시 파일을 저장하는게 아닌 이름변경 기록을 txt형태로 저장하여 관리
# TODO 중복된 이름 발생시 발생하는 오류 제거
def filename_change(start_name, end_name, logstat=False):
    # print(start_name, end_name)

    if logstat and (not os.path.exists(log_folder_name)):
        os.mkdir(log_folder_name)

    if os.path.isfile(start_name):
        _, ext = os.path.splitext(start_name)
        end_file_name, _ = os.path.splitext(end_name)
        os.rename(start_name, end_file_name + ext)


def main_cc(file, delay, logstat, time_start=None, time_end=None):
    select_stat = True

    if logstat and (not os.path.exists(log_folder_name)):
        os.mkdir(log_folder_name)

    if os.path.isfile(file):
        _, ext = os.path.splitext(file)

        if ext == ".ass" or ext == ".smi":
            if logstat:
                log_file = os.path.join(log_folder_name, file)
                if not os.path.exists(log_file):
                    shutil.copy2(file, log_file)
                else:
                    print("이미 존재하는 로그 파일입니다. \n덮어 쓰시겠습니까?")
                    if not select_stat:
                        return

            if ext == ".ass":
                sync_ass(file, delay, time_start, time_end)
            elif ext == ".smi":
                print("ext : smi")
                sync_smi(file, delay, time_start, time_end)
