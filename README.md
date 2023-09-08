# From pictures to video via Python's ffmpeg package.


### Main function: Zoom in, Pan over, and Zoom out
You can directly use the main_function.py file. It takes several arguments from command line  

- in_filename
- --point_a POINT_A 
- --point_b POINT_B  
- --point_c POINT_C


Example: ```python main_function.py your_image_name.jpg --point_a 1489,278 --point_b 467,371```

### Pan over function
The pan_over.py file under the script folder takes the same arguments as the main function. The difference is pan_over doesn't include the zoom in and zoom out effects before and after the panover.

### Add Audio
You can add the background audio as you want to a video. The function is in the add_audio.py under the script folder.


### Concatenate Videos
You can concatenate as much videos as you want by using the concatenate.py file under the script folder. Add all the file names into the out_videos list. 

