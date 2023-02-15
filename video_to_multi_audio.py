import os, sys
import subprocess
import argparse
import json

# argparse template
parser = argparse.ArgumentParser(description='Convert video to multi audio')
parser.add_argument('input', help='input video file')

args = parser.parse_args()


dir_of_original_file = os.path.dirname(args.input)
filename_of_original_file = os.path.basename(args.input)
filename_of_original_file_without_extension = os.path.splitext(filename_of_original_file)[0]

out_dir = os.path.join(dir_of_original_file, filename_of_original_file_without_extension+"_outaudios")
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

# get tmp audio file
raw_audio_path = os.path.join(out_dir, 'raw_audio.mp3')
subprocess.call(['ffmpeg', '-i', args.input, '-f','mp3','-vn', raw_audio_path])

# get audio time by ffprobe
command = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format','-show_streams', raw_audio_path]
total_seconds = float(json.loads(subprocess.check_output(command))['format']['duration'])


# Split to multiple audios
def total_seconds_to_time_turation(s):
    num_list = []
    res_list = []
    D = [800,900,1000,1100]
    for dur in [800,900,1000,1100]:
        num,res = divmod(s,dur)
        num_list.append(num)
        res_list.append(res)
    _i = res_list.index(max(res_list))
    print(f"============================= set time duration to{D[_i]}")
    return D[_i],num_list[_i],res_list[_i]
    

D,_,_ = total_seconds_to_time_turation(total_seconds)
subprocess.call(['ffmpeg', '-i', raw_audio_path, '-f','segment','-segment_time',str(D),'-c','copy', os.path.join(out_dir, r'out%03d.mp3')])



# upload to web
# https://www.luyinzhushou.com/voice2text/   


#
con = input("请复制所有转换得到的txt到音频的文件夹中, 按 y 开始合并: ")
if con.lower() == "y":
    filename_list = []
    for item in os.listdir(out_dir):
        if item.endswith(".txt"):
            filename_list.append(item)
    
    filename_list.sort()
    # merge txt
    with open(os.path.join(out_dir, "all.txt"), "w") as f:
        for file in filename_list:
            with open(os.path.join(out_dir, file), "r") as f1:
                f.write(f1.read())
    
    print(f"FINAL: {os.path.join(out_dir, 'all.txt')}")
else:
    print("Bye~ :)")