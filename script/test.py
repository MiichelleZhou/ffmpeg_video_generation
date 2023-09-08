import os
from PIL import Image

def cmd_execute(cmd_str=""):
    print("Executing cmd: {}".format(cmd_str))
    with os.popen(cmd_str) as f:
        cmd_output = str.join("\n", f.readlines())

    if cmd_output is not None and len(cmd_output) !=0:
        print("cmd_output: {}".format(cmd_output))
        return False
    return True


def zoominout():
    cmd = f'''ffmpeg -loop 1 -i ./pics/piano.jpg -i ./audio/sample.mp3 -vf "[0:v]scale=7680x4320,zoompan=z='if(gte(zoom,1.5)+eq(ld(1),1)*gt(zoom,1),zoom-0.00005*st(1,1),zoom+0.00005+st(1,0))':d=20000" -c:a copy -c:v libx264 -shortest out3.mp4'''
    return cmd



cmd_output_in = cmd_execute(zoominout())