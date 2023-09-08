import os
import argparse
from PIL import Image


def cmd_execute(cmd_str=""):
    print("Executing cmd: {}".format(cmd_str))
    with os.popen(cmd_str) as f:
        cmd_output = str.join("\n", f.readlines())

    if cmd_output is not None and len(cmd_output) !=0:
        print("cmd_output: {}".format(cmd_output))
        return False
    return True


# zoom into a certain point from the whole frame
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


# zoom out to the whole frame from a certain point 
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


# resize the image; return true/false
def resize_image(in_img_path, out_img_path, out_size=(0, 0)):
    try:
        in_image = Image.open(in_img_path)
    except:
        print("Error! resize_image(): open image {}".format(in_img_path))
        return False

    if out_size is None:
        image_size_origin = in_image.size
        # make size even, otherwise error when specify video size
        out_size = (
            image_size_origin[0] + 1 if (image_size_origin[0] % 2 == 1) else image_size_origin[0],
            image_size_origin[1] + 1 if (image_size_origin[1] % 2 == 1) else image_size_origin[1]
        )
        print("resize_image(): auto-adjusted output size {}".format(out_size))
    else:
        # check if output size is even， if not adjust to even
        if (out_size[0] % 2 == 1) or (out_size[1] % 2 == 1):
            origin_out_size = out_size
            out_size = (
                origin_out_size[0] + 1 if (origin_out_size[0] % 2 == 1) else origin_out_size[0],
                origin_out_size[1] + 1 if (origin_out_size[1] % 2 == 1) else origin_out_size[1]
            )
            print("resize_image(): Invalid output size {}! auto-adjusted output size {}.".format(origin_out_size,
                                                                                                 out_size))
    out_img = in_image.resize(out_size, Image.ANTIALIAS)
    # out_img = in_image.resize(out_size, Image.Resampling.LANCZOS)
    out_img.save(out_img_path)
    return True


# zoom in, move from point A to point B
def vf_zoom_move(in_file="", out_file="", out_size=(0, 0), point_start=(0, 0), point_end=(0, 0), z_effect=1, time=0,
                 move_speed=1):
    scale_ratio = 10
    upscale = f"{out_size[0] * scale_ratio}x{out_size[1] * scale_ratio}"
    out_scale = f"{out_size[0]}x{out_size[1]}"
    frame_rate = 25 * time
    move_frame_rate = frame_rate / move_speed
    vf_str = f'''
        scale={upscale},
        zoompan=
            x='({point_start[0]}+(on/{move_frame_rate})*({point_end[0] - point_start[0]}))*{scale_ratio}*(1-1/zoom):
            y='({point_start[1]}+(on/{move_frame_rate})*({point_end[1] - point_start[1]}))*{scale_ratio}*(1-1/zoom)':
            z='{z_effect}':
            d={frame_rate}:
            s={out_scale}
    '''
    return "ffmpeg -y -i {0} -vf \"{2}\" -pix_fmt yuv420p -c:v libx264 {1}".format(in_file, out_file,vf_str.replace("\n", "").replace(" ",""))



# stop n seconds
def vf_stop_effect(in_file="", out_file="", time=0):
    return f"ffmpeg -y -framerate 25 -loop 1 -i {in_file} -c:v libx264 -t {time} -pix_fmt yuv420p {out_file}"


# stop extract last or begin frame
def vf_extract_frame(in_file="", out_file="", frame="last"):
    ffmpeg_cmd = None
    if frame == "last":
        ffmpeg_cmd = f"ffmpeg -y -sseof -0.1 -i {in_file} -q:v 2 -update 1 {out_file}"
    elif frame == "first":
        ffmpeg_cmd = f"ffmpeg -y -i {in_file} -vf \"select=eq(n\,0)\" -q:v 3 {out_file}"
    return ffmpeg_cmd


# concat videos
def vf_concat_videos(in_files=[], out_file=""):
    list_file = 'concat_videos.txt';
    with open(list_file, 'w') as fh:
        for filename in in_files:
            if isinstance(filename, str) and filename.endswith('.mp4'):
                print(filename)
                fh.write("file '{}'\n".format(filename))
    return "ffmpeg -f concat -safe 0 -y -i {} -c copy {}".format(list_file, out_file)



def main_function():
    parser = argparse.ArgumentParser(description="Process video and image files.")
    parser.add_argument('in_filename', type=str, help='Input filename')
    parser.add_argument('--point_a', type=lambda s: tuple(map(int, s.split(','))),  help='Point A in format x,y')
    parser.add_argument('--point_b', type=lambda s: tuple(map(int, s.split(','))),  help='Point B in format x,y')
    parser.add_argument('--point_c', type=lambda s: tuple(map(int, s.split(','))),  help='Point C in format x,y')
    args = parser.parse_args()
    out_videos = []    
    
    # step0: get input image
    in_filename_base = os.path.splitext(args.in_filename)[0]
    in_file = "./image/{}".format(args.in_filename)
    resized_image_file = "./out/{}_resize.jpg".format(in_filename_base)
    
    # step1: resize image
    out_size = (1920, 1280)
    result = resize_image(in_file, resized_image_file, out_size)
    if result:
        print("Success! Resize output image file: {}".format(resized_image_file))
    else:
        print("Failure! Resize input image file: {}".format(in_file))
    

    # step2: move into the starting point 
    z_end = 2.8
    zoom_in_file = "./out/zoom_in.mp4"
    time = 4

    ff_cmd_in = vf_zoom(
        in_file=in_file,
        out_file=zoom_in_file,
        image_size=out_size,
        z_point= args.point_a,
        z_end=z_end,
        time=time)
    cmd_output_in = cmd_execute(ff_cmd_in)  


    # step3: move from point A to point B
    out_file2 = "./out/{}_move1.mp4".format(in_filename_base)
    point_a = args.point_a
    point_b = args.point_b
    z_multi = 2.8
    time = 4
    move_speed = 1
    ff_cmd = vf_zoom_move(in_file=resized_image_file
                          , out_file=out_file2
                          , out_size=out_size
                          , point_start=point_a
                          , point_end=point_b
                          , z_effect=z_multi
                          , time=time
                          , move_speed=move_speed
                          )
    cmd_output = cmd_execute(ff_cmd)
    out_videos.append(out_file2)

    # step4: extract the last frame and make a video for n seconds
    in_file3 = out_file2
    out_file3 = "./out/{}_extract_frame.jpg".format(in_filename_base)
    ff_cmd = vf_extract_frame(in_file=in_file3, out_file=out_file3, frame="last")
    cmd_output = cmd_execute(ff_cmd)
    # make a video for n seconds
    out_file4 = "./out/{}_extract_frame.mp4".format(in_filename_base)
    time = 1
    ff_cmd = vf_stop_effect(in_file=out_file3, out_file=out_file4, time=time)
    cmd_output = cmd_execute(ff_cmd)
    out_videos.append(out_file4)
   
    # step5: move from point B to point C
    out_file5 = "./out/{}_move2.mp4".format(in_filename_base)
    # point_a = (467, 371)
    # point_b = (1274, 580)
    point_a = args.point_b
    point_b = args.point_c

    z_multi = 2.8
    time = 4
    move_speed = 1

    ff_cmd = vf_zoom_move(in_file=resized_image_file
                          , out_file=out_file5
                          , out_size=out_size
                          , point_start=point_a
                          , point_end=point_b
                          , z_effect=z_multi
                          , time=time
                          , move_speed=move_speed
                          )
    cmd_output = cmd_execute(ff_cmd)
    out_videos.append(out_file5)

    # step6: zoom out from the last point to the whole frame
    z_end = 2.8
    zoom_in_file = "./out/zoom_in_temp.mp4"
    time = 4
    ff_cmd_in = vf_zoom(
        in_file=in_file,
        out_file=zoom_in_file,
        image_size=out_size,
        z_point= args.point_c,
        z_end=z_end,
        time=time)
    cmd_output_in = cmd_execute(ff_cmd_in)
    zoom_out_file = "./out/zoom_out.mp4"
    reverse_cmd = reverse_video(in_file=zoom_in_file, out_file=zoom_out_file)
    cmd_output_reverse = cmd_execute(reverse_cmd)

    # step7: concat videos to final video
    out_file_final = "./out/{}_final.mp4".format(in_filename_base)
    ff_cmd = vf_concat_videos(in_files=out_videos, out_file=out_file_final)
    print(ff_cmd)
    cmd_output = cmd_execute(ff_cmd)
    print(cmd_output)
    out_videos = [zoom_in_file, out_file_final, zoom_out_file]
    ff_cmd = vf_concat_videos(in_files=out_videos, out_file='./final/out_file_final.mp4')
    print(ff_cmd)
    cmd_output = cmd_execute(ff_cmd)
    print("Done!")


if __name__ == '__main__':
   main_function()
