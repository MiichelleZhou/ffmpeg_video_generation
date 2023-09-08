import os
from PIL import Image

def vf_zoom(in_file="", out_file="", image_size=(0, 0), z_point=(0, 0), z_end=1, time=1):
    # Calculate total frames needed
    frame_count = 25 * time  # Assuming 25fps
    
    vf_str = "scale=-2:{2},zoompan=z='zoom+({4}-1)/{5}':x='if(lte(zoom,1.0),0,(iw-iw/zoom)*({0}/{2}))':y='if(lte(zoom,1.0),0,(ih-ih/zoom)*({1}/{3}))':d={5}:s={2}x{3}:fps=25".format(
        z_point[0],
        z_point[1],
        image_size[0],
        image_size[1],
        z_end,
        frame_count
    )
    return "ffmpeg -y -i {0} -vf \"{2}\" -pix_fmt yuv420p -c:v libx264 {1}".format(in_file, out_file, vf_str)

def vf_zoom_out(in_file="", out_file="", image_size=(0, 0), z_point=(0, 0), z_start=2.8, time=1):
    # Calculate total frames needed
    frame_count = 25 * time  # Assuming 25fps

    vf_str = ("scale=-2:{2},zoompan=z='if(gte(zoom,{4}),max(1,zoom-({4}-1)/{5}),1)':"
              "x='(iw-iw/zoom)*({0}/{2})':y='(ih-ih/zoom)*({1}/{3})':"
              "d={5}:s={2}x{3}:fps=25").format(
        z_point[0],
        z_point[1],
        image_size[0],
        image_size[1],
        z_start,
        frame_count
    )
    return "ffmpeg -y -i {0} -vf \"{2}\" -pix_fmt yuv420p -c:v libx264 {1}".format(in_file, out_file, vf_str)

def cmd_execute(cmd_str=""):
    print("Executing cmd: {}".format(cmd_str))
    with os.popen(cmd_str) as f:
        cmd_output = str.join("\n", f.readlines())

    if cmd_output is not None and len(cmd_output) !=0:
        print("cmd_output: {}".format(cmd_output))
        return False
    return True


def reverse_video(in_file="", out_file=""):
    cmd = f"ffmpeg -y -i {in_file} -vf reverse -af areverse {out_file}"
    return cmd


out_size = (1920, 1280)
z_end = 2.8
time = 4
in_file = "./pics/windows-people.jpg"
zoom_in_file = "./test/zoom_in_temp.mp4"

ff_cmd_in = vf_zoom(
    in_file=in_file,
    out_file=zoom_in_file,
    image_size=out_size,
    z_point=(1274, 580),
    z_end=z_end,
    time=time
)

cmd_output_in = cmd_execute(ff_cmd_in)


zoom_out_file = "./test/zoom_out_test.mp4"
reverse_cmd = reverse_video(in_file=zoom_in_file, out_file=zoom_out_file)
cmd_output_reverse = cmd_execute(reverse_cmd)
