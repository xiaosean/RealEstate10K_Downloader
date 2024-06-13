import os
import sys
import glob
import argparse
from time import sleep
import random
from multiprocessing import Pool
from PIL import Image
import numpy as np
import yt_dlp as youtube_dl  # Using yt_dlp instead of youtube_dl
import subprocess


class Data:
    def __init__(self, url, seqname, list_timestamps):
        self.url = url
        self.list_seqnames = []
        self.list_list_timestamps = []
        self.list_seqnames.append(seqname)
        self.list_list_timestamps.append(list_timestamps)

    def add(self, seqname, list_timestamps):
        self.list_seqnames.append(seqname)
        self.list_list_timestamps.append(list_timestamps)

    def __len__(self):
        return len(self.list_seqnames)


def check_ffmpeg_installed():
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("[INFO] ffmpeg is installed.")
            print(result.stdout)
        else:
            print("[ERROR] ffmpeg is not installed correctly.")
            print(result.stderr)
    except FileNotFoundError:
        print("[ERROR] ffmpeg command not found. Please install ffmpeg.")


def process(data, seq_id, videoname, output_root, resized_height, resized_width):
    
    seqname = data.list_seqnames[seq_id]
    seq_output_dir = os.path.join(output_root)
    if not os.path.exists(seq_output_dir):
        os.makedirs(seq_output_dir)
    
    # Resize the video using ffmpeg, and save the resized mp4
    subprocess.run([
        'ffmpeg', '-i', videoname,
        '-vf', f'scale={resized_width}:{resized_height}',
        f'{seq_output_dir}/{videoname}'
    ])

    # if you want to extract frame by frame
    
    # list_str_timestamps = []
    # for timestamp in data.list_list_timestamps[seq_id]:
    #     timestamp = int(timestamp / 1000)
    #     str_hour = str(int(timestamp / 3600)).zfill(2)
    #     str_min = str(int(int(timestamp % 3600) / 60)).zfill(2)
    #     str_sec = str(int(int(int(timestamp % 3600) % 60) / 1)).zfill(2)
    #     str_mill = str(int(int(int(timestamp % 3600) % 60) % 1)).zfill(3)
    #     _str_timestamp = str_hour + ":" + str_min + ":" + str_sec + "." + str_mill
    #     list_str_timestamps.append(_str_timestamp)
    

    # for idx, str_timestamp in enumerate(list_str_timestamps):
    #     output_filename = os.path.join(seq_output_dir, f"{data.list_list_timestamps[seq_id][idx]}.png")
    #     # command = ['ffmpeg', '-ss', str_timestamp, '-i', videoname, '-vframes', '1', '-f', 'image2', output_filename]
    #     # command = ['ffmpeg', '-ss', str_timestamp, '-i', videoname, '-vframes', '1', '-f', 'image2', output_filename]
    #     # command = ['ffmpeg', '-i', videoname, '-r', '1', '-f', 'image2', output_filename]
    #     print(f"Executing command: {' '.join(command)}")  # Debug info
    #     result = subprocess.run(command, capture_output=True, text=True)
    #     if result.returncode != 0:
    #         print(f"[ERROR] ffmpeg failed: {result.stderr}")
    #         return True
    #     else:
    #         print(f"[INFO] ffmpeg output: {result.stdout}")  # Debug info

        # Check if the file was created
    #     if not os.path.exists(output_filename):
    #         print(f"[ERROR] File not created: {output_filename}")
    #         return True

    # png_list = glob.glob(os.path.join(seq_output_dir, "*.png"))
    # if not png_list:
    #     print("[ERROR] No PNG files found, something went wrong.")
    #     return True

    # for pngname in png_list:
    #     image = Image.open(pngname)
    #     image_resized = image.resize((resized_width, resized_height), Image.ANTIALIAS)
    #     image_resized.save(pngname)

    
    # return False

def wrap_process(list_args):
    return process(*list_args)


class DataDownloader:
    def __init__(self, dataroot, mode='test', resized_height=360, resized_width=640, retry=False):
        print("[INFO] Loading data list ... ", end='')
        self.dataroot = dataroot
        self.mode = mode
        self.output_root = './dataset/' + mode + '/video/'
        self.resized_height = resized_height
        self.resized_width = resized_width
        self.isDone = False

        # Create mode directory if it doesn't exist
        if not os.path.exists(self.output_root):
            os.makedirs(self.output_root)
            print(f"[INFO] Created directory: {self.output_root}")
        else:
            print("[INFO] The output dir has already existed.")
            self.isDone = True

        self.list_seqnames = sorted(glob.glob(dataroot + '/*.txt'))
        self.list_data = []

        if retry:
            self.load_failed_videos()
        else:
            self.load_data_list()
        print(" Done! ")
        print("[INFO] {} movies are used in {} mode".format(len(self.list_data), self.mode))

    def load_data_list(self):
        for txt_file in self.list_seqnames:
            dir_name = txt_file.split('/')[-1]
            seq_name = dir_name.split('.')[0]
            with open(txt_file, "r") as seq_file:
                lines = seq_file.readlines()
                youtube_url = lines[0].strip()
                list_timestamps = [int(line.split(' ')[0]) for line in lines[1:]]

            isRegistered = False
            for i in range(len(self.list_data)):
                if youtube_url == self.list_data[i].url:
                    isRegistered = True
                    self.list_data[i].add(seq_name, list_timestamps)
                    break

            if not isRegistered:
                self.list_data.append(Data(youtube_url, seq_name, list_timestamps))

    def load_failed_videos(self):
        failed_log_path = f'failed_videos_{self.mode}.txt'
        if os.path.exists(failed_log_path):
            with open(failed_log_path, 'r') as f:
                seqnames = [seqname.strip() for seqname in f.readlines()]
            for seqname in seqnames:
                txt_file = os.path.join(self.dataroot, seqname + '.txt')
                if os.path.exists(txt_file):
                    dir_name = txt_file.split('/')[-1]
                    seq_name = dir_name.split('.')[0]
                    with open(txt_file, "r") as seq_file:
                        lines = seq_file.readlines()
                        youtube_url = lines[0].strip()
                        list_timestamps = [int(line.split(' ')[0]) for line in lines[1:]]

                    isRegistered = False
                    for i in range(len(self.list_data)):
                        if youtube_url == self.list_data[i].url:
                            isRegistered = True
                            self.list_data[i].add(seq_name, list_timestamps)
                            break

                    if not isRegistered:
                        self.list_data.append(Data(youtube_url, seq_name, list_timestamps))
                else:
                    print(f"[ERROR] Failed txt file {txt_file} not found.")
        else:
            print(f"[ERROR] Failed log file {failed_log_path} not found.")

    def Run(self):
        print("[INFO] Start downloading {} movies".format(len(self.list_data)))

        for global_count, data in enumerate(self.list_data):
            for seq_id, seqname in enumerate(data.list_seqnames):
                videoname = f'{seqname}.mp4'
                print(f"[INFO] Downloading {data.url} to {videoname}")
                try:
                    ydl_opts = {
                        'format': 'bestvideo[height<=720][ext=mp4]',
                        'outtmpl': videoname,
                        'merge_output_format': 'mp4',
                        'noplaylist': True,
                        'postprocessor_args': ['-an'],  # Remove audio
                    }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([data.url])
                except Exception as e:
                    print(f"[ERROR] Failed to download {data.url}: {e}")
                    with open('failed_videos_' + self.mode + '.txt', 'a') as failure_log:
                        failure_log.writelines(seqname + '\n')
                    continue

                # Add a delay to avoid too many requests
                sleep(random.uniform(5, 10))

                if not os.path.exists(videoname):
                    print("[ERROR] Video file not found for url:", data.url)
                    with open('failed_videos_' + self.mode + '.txt', 'a') as failure_log:
                        failure_log.writelines(seqname + '\n')
                    continue
                # if you want to extract to frame
                process(data, seq_id, videoname, self.output_root, self.resized_height, self.resized_width)
                os.remove(videoname)
                

                if self.isDone:
                    return False

        return True

    def Show(self):
        print("########################################")
        global_count = 0
        for data in self.list_data:
            print(" URL : {}".format(data.url))
            for idx in range(len(data)):
                print(" SEQ_{} : {}".format(idx, data.list_seqnames[idx]))
                print(" LEN_{} : {}".format(idx, len(data.list_list_timestamps[idx])))
                global_count += 1
            print("----------------------------------------")

        print("TOTAL : {} sequences".format(global_count))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RealEstate10K Downloader")
    parser.add_argument("mode", choices=["test", "train"], help="Mode: test or train")
    parser.add_argument("--height", type=int, default=256, help="Height of resized images")
    parser.add_argument("--width", type=int, default=384, help="Width of resized images")
    parser.add_argument("--retry", action='store_true', help="Retry failed downloads")

    args = parser.parse_args()

    dataroot = "./RealEstate10K/" + args.mode
    check_ffmpeg_installed()
    downloader = DataDownloader(dataroot, args.mode, args.height, args.width, args.retry)
    downloader.Show()
    isOK = downloader.Run()

    if isOK:
        print("Done!")
    else:
        print("Failed")
