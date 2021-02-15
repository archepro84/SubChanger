import os
import re
import shutil

search_path = r"caption_file\Test_only"
os.chdir(search_path)
log_folder_name = "pre_log"

for data in os.listdir():
    if not os.path.exists(log_folder_name):
        os.mkdir(log_folder_name)

    if os.path.isfile(data):
        _, ext = os.path.splitext(data)
        if ext == ".ass":
            print("file ext = .ass")
            if not os.path.exists(os.path.join(log_folder_name, data)):
                shutil.copy2(data,
                             os.path.join(log_folder_name, data))

            else:
                print("이미 존재하는 로그 파일입니다. \n덮어 쓰시겠습니까?")
                pass

        elif ext == ".smi":
            print("file ext = .smi")

    elif os.path.isdir(data):
        print("dir", data)
    else:
        print("is not found")
