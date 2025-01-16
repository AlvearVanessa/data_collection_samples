"""
Recording videos from 3 cameras in specifics folder:
Camera Intel RealSense D457 RGB and Depth
Microsoft LifeCam HD-3000
Logitech Brio Webcam 4k UltraHD

Based on the GitHub website:
https://github.com/nicknochnack/ActionDetectionforSignLanguage

@uthors:
manuel_garcia_dominguez (manuel.garciad@unirioja.es),
miren_mirari_san_martin (miren.san-martin@unirioja.es),
mayra_vanessa_alvear (maalvear@unirioja.es)

May, 15 2024 13:36h CET

This code recorder videos from 3 cameras (one of them record
two videos from rgb and depth images) for a total of 4 videos per shot,
shows the number of frames in the corner,
the name of the class, the video number,
and a chronometer.
Each video has a duration of 7 seconds.
It creates a folder per class and save the corresponding video of the class.
Only saves the video without text showing on the screen during the recorder
which was made to help the person.
"""

# Import libraries
import cv2
import os
import time
import numpy as np
import pyrealsense2 as rs

# For multiple cameras
cameras_folders = ['CAMERA_1','CAMERA_2','Camera_realsense']

# Identification number for the person recorder
person_id = "001"

# Classes
actions = ['PRUEBA']

# Realsense setup
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.color, 640,480, rs.format.rgb8, 30)
cfg.enable_stream(rs.stream.depth, 640,480, rs.format.z16, 30)
pipe.start(cfg)

# Capture the image from camera 1
vid_capture = cv2.VideoCapture(0)

# Capture the image from camera 2
vid_capture2 = cv2.VideoCapture(1)

# In case there is no camera
if (vid_capture.isOpened() == False):
    print("Unable to read camera feed")


# Setting sizes 3 and 4 are Id's to width and height
vid_cod = cv2.VideoWriter_fourcc(*'mp4v')
width = int(vid_capture.get(3))
height = int(vid_capture.get(4))
size = (width, height)

# Parameters
# Number of videos worth of data
no_sequences = 6
# Videos are going to be 30 frames in length
frame_per_sec = 30


def record_video(classes, cam_folders):
    """
    Function to record a sequence of videos in a corresponding folder
    which each folder is created based on the class name

    :param classes: list of the classes name
    :param cam_folders: list of the camera names
    :return: a folder named CAMERA_1, CAMERA_2, Camera_realsense with 2 videos per class
             recorder in real-time.
    """
    list_paths = []

    pTime = 0
    for folder in cam_folders:
        # source_path = os.path.join('.\PRUEBA/')
        source_path = os.path.join("." + "\\" + folder + "/")
        # Adding strings of the source paths
        list_paths.append(source_path)
        # Create folder per action
        for action in actions:
            try:
                os.makedirs(os.path.join(source_path, action))
            except:
                pass

    for object1 in classes:
        # Loop through sequences aka videos
        for sequence in range(no_sequences):

            # Get the dominant hand for video recording
            if (sequence < int(no_sequences / 2)):
                hand = "right"
            else:
                hand = "left"

            # Loop through video length aka sequence length
            new = os.path.join(list_paths[0] + object1 + '/')

            # Second camera
            cam2 = os.path.join(list_paths[1] + object1 + '/')
            realsense = os.path.join(list_paths[2] + object1 + '/')

            # Codec definition
            # First Cam
            output = cv2.VideoWriter(new + "video_"+ person_id+ "_" +str(sequence) + '_' + "camera1_" + str(object1) + "_"+ hand +"Hand.mp4",
                                     vid_cod, frame_per_sec, (width, height))
            # Second camera
            output2 = cv2.VideoWriter(cam2 + "video_"+ person_id+ "_" + str(sequence) + '_' + "camera2_" + str(object1) + "_"+ hand +"Hand.mp4",
                                     vid_cod, frame_per_sec, (width, height))
            # RealSense RGB Camera
            output3_RGB = cv2.VideoWriter(
                realsense + "RGBvideo_"+ person_id+ "_" + str(sequence) + '_' + "camera3_" + str(object1) + "_"+ hand +"Hand.mp4", vid_cod, frame_per_sec, size)
            # RealSense Depth Camera
            output3_depth = cv2.VideoWriter(
                realsense + "depthvideo_"+ person_id+ "_" + str(sequence) + '_' + "camera3_" + str(object1) + "_"+ hand +"Hand.mp4", vid_cod, frame_per_sec, size)

            # Just to record 7 seconds of video
            for frame_num in range(frame_per_sec * 7):

                # Chronometer
                sec = int(frame_num/frame_per_sec)

                # Read camera 1 info
                ret, frame = vid_capture.read()
                output.write(frame)

                # Read camera 2 info
                ret2, frame2 = vid_capture2.read()
                output2.write(frame2)

                # Read camera Intel RS info
                # Realsense frame acquisition
                frame_realsense = pipe.wait_for_frames()
                depth_frame = frame_realsense.get_depth_frame()
                color_frame = frame_realsense.get_color_frame()

                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,
                                                                 alpha=0.5), cv2.COLORMAP_JET)
                gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
                color_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

                output3_RGB.write(color_image)
                output3_depth.write(depth_cm)

                # Apply wait logic
                if frame_num == 0:
                    # To print in screen when starts to record
                    cv2.putText(frame, 'STARTING COLLECTION 0', (120, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.putText(frame, 'CAM_1 Class {} Number {}'.format(object1, sequence),
                                (20, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                                cv2.LINE_AA)
                    cv2.putText(frame, 'Hand {}'.format(hand), (20, 70), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 3, cv2.LINE_AA)  # .format(list_paths[0], object1, sequence),
                    # Second camera
                    # cv2.putText(frame2, 'STARTING COLLECTION 0', (120, 200),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    # cv2.putText(frame2, 'CAM_2 Class {} Number {}'.format(object1, sequence),
                    #             (20, 35),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                    #             cv2.LINE_AA)

                    # Adding frame rate
                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime

                    cv2.putText(frame, f'FPS:{int(fps)}', (473, 35), cv2.FONT_HERSHEY_PLAIN,
                                3, (0, 0, 255), 3)

                    # Second camera
                    # cv2.putText(frame2, f'FPS:{int(fps)}', (473, 35), cv2.FONT_HERSHEY_PLAIN,
                    #             3, (0, 0, 255), 3)

                    # Show to screen
                    cv2.imshow('OpenCV Feed', frame)
                    # Second camera
                    #cv2.imshow('OpenCV Feed', frame2)
                    cv2.waitKey(100)

                else:
                    cv2.waitKey(3)
                    cv2.putText(frame, 'RECORDING', (120, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    cv2.putText(frame, 'CAM_1 Class {} Number {}'.format(object1, sequence),
                                (20, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                                cv2.LINE_AA)
                    cv2.putText(frame, 'Hand {}'.format(hand), (20, 70), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 3, cv2.LINE_AA)  # .format(list_paths[0], object1, sequence),

                    # Second camera
                    #cv2.putText(frame2, 'RECORDING', (120, 200),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    #cv2.putText(frame2, 'CAM_1 Class {} Number {}'.format(object1, sequence),
                    #             (20, 35),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                    #             cv2.LINE_AA)

                    # Adding frame rate
                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime

                    cv2.putText(frame, f'FPS:{int(fps)}', (473, 35), cv2.FONT_HERSHEY_PLAIN,
                                3, (0, 0, 255), 3)

                    # Chronometer
                    cv2.putText(frame, 'sec {} '.format(sec),
                                (width-110, height-20),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                                cv2.LINE_AA)

                    # Second camera
                    cv2.putText(frame2, f'FPS:{int(fps)}', (473, 35), cv2.FONT_HERSHEY_PLAIN,
                                3, (0, 0, 255), 3)

                                # Show to screen
                    cv2.imshow('OpenCV Feed', frame)

                    # Second camera
                    #cv2.imshow('OpenCV Feed', frame2)

                    # cv2.imshow('OpenCV Feed', frame1)
                    # cv2.imshow('OpenCV Feed', color_image)
                    # cv2.imshow('OpenCV Feed', depth_cm)

            # Close and break the loop after pressing "x" key
            if cv2.waitKey(1) & 0XFF == ord('x'):

                break

    # close the already opened camera
    vid_capture.release()
    output.release()
    output3_RGB.release()
    output3_depth.release()

    # Second camera
    vid_capture2.release()
    output2.release()
    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

# Call the function
record_video(actions, cameras_folders)