"""
Recording videos from 1 webcam in specific folder

Source
Course: Hand Sign Detection for vowels of the American Sign Language
Based on: Computer Vision Zone
Website: https://www.computervision.zone/courses/hand-sign-detection-asl/


@utor: maalvear
April, 25 2024 15:03h CET

This code make a video recorder from 1 camera,
shows the number of frames in the corner.
Create a folder per class and save the corresponding video of the class.
Only saves the video without text.
"""

# Import libraries
import cv2
import os
import time

# Source path
# cameras_folders = ['CAMERA_1']

# For multiple cameras
cameras_folders = ['CAMERA_1','CAMERA_2']

person_id = "001"


# Classes
actions = ['A', 'E', 'I', 'O', 'U']

# Capture the image from camera 0
vid_capture = cv2.VideoCapture(1)

# Capture the image from camera 1
vid_capture2 = cv2.VideoCapture(2)

# In case there is no camera
if (vid_capture.isOpened() == False):
    print("Unable to read camera feed")

# Parameters
frame_per_sec = 30

# Setting sizes adn 3 and 4 are Id's
width = int(vid_capture.get(3))
height = int(vid_capture.get(4))
size = (width, height)

# Parameters to record video
# Number of videos worth of data
no_sequences = 2
# Videos are going to be 30 frames in length
sequence_length = 30


def record_video(classes, cam_folders):
    """
    Function to record a sequence of videos in a corresponding folder
    which each folder is created base on the class name

    :param classes: list of the classes name
    :param cam_folders: list of the camera names
    :return: a folder named CAMERA_1 with 2 videos per class
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
            # Loop through video length aka sequence length
            new = os.path.join(list_paths[0] + object1 + '/')


            # Second camera
            cam2 = os.path.join(list_paths[1] + object1 + '/')

            # Codec definition
            # output = cv2.VideoWriter(new + "video" + str(sequence) + '_' + "camera1_" + str(object1) + "_rightHand.avi",
                                     # cv2.VideoWriter_fourcc('m', 'j', 'p', 'g'), frame_per_sec, (width, height))
            output = cv2.VideoWriter(new + "video_"+ person_id+ "_" + str(sequence) + '_' + cameras_folders[0]+ str(object1) + "_rightHand.mp4",
                                     cv2.VideoWriter_fourcc(*'mp4v'), frame_per_sec, (width, height))
            # Second camera
            output2 = cv2.VideoWriter(cam2 + "video_"+ person_id+ "_" + str(sequence) + '_' + cameras_folders[1] + str(object1) + "_rightHand.mp4",
                                     cv2.VideoWriter_fourcc(*'mp4v'), frame_per_sec, (width, height))

            # Just to record 7 seconds of video
            for frame_num in range(sequence_length * 7):


                # Chronmeter
                sec = int(frame_num/sequence_length)

                ret, frame = vid_capture.read()
                output.write(frame)

                # Second camera
                ret2, frame2 = vid_capture2.read()
                output2.write(frame2)
                # NEW Apply wait logic
                if frame_num == 0:
                    # To print in screen
                    cv2.putText(frame, 'STARTING COLLECTION 0', (120, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.putText(frame, 'CAM_1 Class {} Number {}'.format(object1, sequence),
                                (20, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                                cv2.LINE_AA)


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
                    # cv2.imshow('OpenCV Feed', frame2)
                    cv2.waitKey(100)

                else:
                    cv2.waitKey(3)
                    cv2.putText(frame, 'RECORDING', (120, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    cv2.putText(frame, 'CAM_1 Class {} Number {}'.format(object1, sequence),
                                (20, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3,
                                cv2.LINE_AA)


                    # Second camera
                    # cv2.putText(frame2, 'RECORDING', (120, 200),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    # cv2.putText(frame2, 'CAM_1 Class {} Number {}'.format(object1, sequence),
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
                    # cv2.putText(frame2, f'FPS:{int(fps)}', (473, 35), cv2.FONT_HERSHEY_PLAIN,

                                # Show to screen
                    cv2.imshow('OpenCV Feed', frame)

                    # Second camera
                    # cv2.imshow('OpenCV Feed', frame2)

                    # cv2.imshow('OpenCV Feed', frame1)

            # Close and break the loop after pressing "x" key
            if cv2.waitKey(1) & 0XFF == ord('x'):
                break

    # close the already opened camera
    vid_capture.release()
    output.release()

    # Second camera
    vid_capture2.release()
    output2.release()
    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()


record_video(actions, cameras_folders)
