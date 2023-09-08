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


def zoom_in_face(image_path):
    ### Face Detection ###
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Load the image
    img = cv2.imread(image_path)
    # Convert color image to grayscale and detect face
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayscale_img, 1.1, 4)
    face_locations = []
    for (x, y, w, h) in faces:
        print(f'Face found. Position: x={x} y={y} width={w} height={h}')
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_locations.append((x, y, w, h))  # Adding the face location as a tuple to the list
    cv2.imshow('img', img)
    cv2.waitKey(30)
    x_coord = 1120 + 50
    y_coord = 450 - 50
    
    ### Video Generation ###
    generate_zoom_video(image_path, './out/zoom_video_3.mp4', x_coord, y_coord, zoom=1.5)
    print("Successfully generated video")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("image_path", help="The path of the input image.")
    # args = parser.parse_args()
    # zoom_in_face(args.image_path)
    generate_zoom_video('./pics/windows-people.jpg', './out/zoom_people.mp4', 1489,278, zoom=2.8)
