import os
import myNote.CaptionProject.caption_change as cc

delay = 1000
search_path = r"G:\Code_program\PyhtonProject\myNote\caption_file"
os.chdir(search_path)

if __name__ == "__main__":
    for file in os.listdir(os.getcwd()):
        print(file)
        cc.main_cc(file, delay, True)
