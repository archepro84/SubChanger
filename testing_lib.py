import os
import myNote.SubChanger.Qtlib.sub_change as cc

delay = 60000
# search_path = r"G:\Code_program\PyhtonProject\myNote\caption_file"
search_path = r"C:\PythonProject\myNote\SubChanger\caption_file"

os.chdir(search_path)

if __name__ == "__main__":
    # for file in os.listdir(os.getcwd()):
    #     print(file)
    #     cc.main_cc(file, delay, False)
    # cc.main_cc("페아포 1화.ass", delay, False, 120000, 1600000)
    # cc.sync_smi("Psycho-Pass 3 - 06 (BD 1280x720 x264 AAC).smi", delay)
    # cc.sync_smi("Psycho-Pass 3 - 06 (BD 1280x720 x264 AAC).smi", delay, 20000, 1440000)
    file_name = ['temp 1.avi', 'temp 2.avi', 'temp 3.avi', 'temp 4.mp4', 'temp 5.mp4', 'temp 6.mp4']
    subtitle_name = ['Psycho-Pass 3 - 06 (BD 1280x720 x264 AAC).smi', 'Psycho-Pass 3 - 07 (BD 1280x720 x264 AAC).smi',
                     'Psycho-Pass 3 - 08 (BD 1280x720 x264 AACx2).smi', '페아포 1화.ass', '페아포 2화.ass', '페아포 3화.ass']
    for i in range(len(file_name)):
        cc.filename_change(subtitle_name[i], file_name[i])


