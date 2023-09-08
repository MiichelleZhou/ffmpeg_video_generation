import os

def vf_concat_videos(in_files=[], out_file=""):
    list_file = 'concat_videos.txt';
    with open(list_file, 'w') as fh:
        for filename in in_files:
            if isinstance(filename, str) and filename.endswith('.mp4'):
                print(filename)
                fh.write("file '{}'\n".format(filename))
    return "ffmpeg -f concat -safe 0 -y -i {} -c copy {}".format(list_file, out_file)


def cmd_execute(cmd_str=""):
    print("Executing cmd: {}".format(cmd_str))
    with os.popen(cmd_str) as f:
        cmd_output = str.join("\n", f.readlines())

    if cmd_output is not None and len(cmd_output) !=0:
        print("cmd_output: {}".format(cmd_output))
        return False
    return True



out_videos = ['./final/zoom_in_people.mp4','./final/people.mp4','./final/zoom_out_people.mp4']
ff_cmd = vf_concat_videos(in_files=out_videos, out_file='./final/out_file_final.mp4')
print(ff_cmd)
cmd_output = cmd_execute(ff_cmd)