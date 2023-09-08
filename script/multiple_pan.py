import cv2
import subprocess
import os
import argparse


### Copyright: by Musicnbrain.org


def generate_zoom_video(image_path, output_path, start_x, start_y, zoom=2.8, duration=100, output_size='1920x1280'):
    command = [
        'ffmpeg', '-y', '-i', image_path,
        '-vf', f'scale=-1:-1,zoompan=x={start_x}:y={start_y}:z=\'if(lte(on,{duration}),(on/{duration})*{zoom}+1, {zoom})\':d={duration}:s={output_size}',
        '-pix_fmt', 'yuv420p', '-c:v', 'libx264', output_path
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)


def generate_video(image_path, output_path, start_x, start_y, end_x, end_y, zoom=2.8, speed=0.6, output_size='1920x1280'):
    duration = int(100 / speed)
    command = [
        'ffmpeg', '-y', '-i', image_path,
        '-vf', f'scale=-1:-1,zoompan=z=\'if(lte(on,{duration}),(on/{duration})*{zoom}+1,{zoom})\':x=\'if(lte(on,{duration}),{start_x}+(on/{duration})*({end_x}-{start_x}),{end_x})\':y=\'if(lte(on,{duration}),{start_y}+(on/{duration})*({end_y}-{start_y}),{end_y})\':d={duration}:s={output_size}',
        '-pix_fmt', 'yuv420p', '-c:v', 'libx264', output_path
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)


def generate_pan_video(image_path, output_path, start_x, start_y, end_x, end_y, duration=100, output_size='1920x1280'):
    width, height = map(int, output_size.split('x'))
    command = [
        'ffmpeg', '-y', '-i', image_path,
        '-vf', f'crop={width}:{height}:x=\'if(gte(n,{duration}),{end_x}, {start_x}+n*(({end_x}-{start_x})/{duration}))\':y=\'if(gte(n,{duration}),{end_y}, {start_y}+n*(({end_y}-{start_y})/{duration}))\'',
        '-pix_fmt', 'yuv420p', '-c:v', 'libx264', output_path
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="The path of the input image.")
    args = parser.parse_args()
    generate_zoom_video(args.image_path, './out/move_video_4.mp4', 1489, 278, zoom=2, speed=0.8, output_size='1920x1280')
