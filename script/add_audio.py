import subprocess



def add_audio_to_video(video_file, start_audio, audio_file, output_file):
    cmd = [
        'ffmpeg', '-y',
        '-i', video_file,
        '-itsoffset', start_audio,
        '-i', audio_file,
        '-map', '0:0',
        '-map', '1:0',
        '-c:v', 'copy',
        '-preset', 'ultrafast',
        '-async', '1',
        output_file
    ]
    subprocess.run(cmd)


def trim_video(input_file, start_time, duration, output_file, both= True):
    if both == True:
        cmd = [
            'ffmpeg', 
            '-i', input_file, 
            '-ss', start_time, 
            '-t', duration, 
            '-c:v', 'copy',
            '-c:a', 'copy',
            output_file
        ]
    else: 
        cmd = [
            'ffmpeg', 
            '-i', input_file, 
            '-ss', start_time, 
            '-t', duration, 
            '-c', 'copy', 
            output_file
        ]
    
    subprocess.run(cmd)

def adjust_volume(input_file, volume_factor, output_file):
    cmd = [
        'ffmpeg', 
        '-i', input_file, 
        '-af', f'volume={volume_factor}',
        '-c:v', 'copy',
        output_file
    ]
    subprocess.run(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("video_file")
    parser.add_argument("audio_file")
    parser.add_argument("start_time")
    parser.add_argument("duration")
    parser.add_argument("volume")
    parser.add_argument("both")


    add_audio_to_video(video_file,start_time, audio_file, "final_1.mp4")
    trim_video('final_1.mp4', start_time, duration, 'final_2.mp4', both)
