import os
import myNote.SubChanger.caption_change as cc

delay = 3000
# search_path = r"G:\Code_program\PyhtonProject\myNote\caption_file"
search_path = r"C:\PythonProject\myNote\SubChanger\caption_file"

os.chdir(search_path)

if __name__ == "__main__":
    # for file in os.listdir(os.getcwd()):
    #     print(file)
    #     cc.main_cc(file, delay, False)
    # cc.sync_specify_smi("페아포 1화.ass", delay)
    # cc.sync_smi("Psycho-Pass 3 - 06 (BD 1280x720 x264 AAC).smi", delay)
    cc.sync_smi("Psycho-Pass 3 - 06 (BD 1280x720 x264 AAC).smi", delay, 20000, 1440000)
