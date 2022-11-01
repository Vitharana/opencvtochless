import cv2
import mediapipe as mp

# Importing Libraries
import serial
import time
xx = 0
yy = 0
t_gap = 0

t_track = False

arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,max_num_hands=1,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():

    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
    image_height, image_width, _ = image.shape
    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # Here is How to Get All the Coordinates
        for ids, landmrk in enumerate(hand_landmarks.landmark):
            # print(ids, landmrk)
            cx, cy = landmrk.x * image_width, landmrk.y*image_height
            #print(cx, cy)
            #print (ids, cx, cy)
            if(ids == 8):
              #print(cx, cy)
              xx = int(cx)
              yy = int(cy)
              image = cv2.circle(image, (60, 240), 60, (255, 255, 0), 5)
              image = cv2.circle(image, (580, 240), 60, (255, 255, 0), 5)
              image = cv2.circle(image, (320, 60), 60, (255, 0, 0), 5)
              image = cv2.circle(image, (320, 420), 60, (255, 0, 0), 5)
              image = cv2.circle(image, (320, 240), 60, (0, 0, 255), 5)




              if(xx >0 and xx<120 and yy>180 and yy<300):
                image = cv2.circle(image, (60, 240), 60, (255, 255, 255), -1)
                arduino.write(bytes("0", 'utf-8'))
                t_track = False
                #time.sleep(0.05)

              elif (xx > 520 and xx < 640 and yy>180 and yy < 300):
                image = cv2.circle(image, (580, 240), 60, (255, 255, 255), -1)
                arduino.write(bytes("2", 'utf-8'))
                t_track = False

              elif (xx > 260 and xx < 380 and yy > 0 and yy < 120):
                image = cv2.circle(image, (320, 60), 60, (255, 255, 255), -1)
                arduino.write(bytes("1", 'utf-8'))
                t_track = False

              elif (xx > 260 and xx < 380 and yy > 360 and yy < 480):
                image = cv2.circle(image, (320, 420), 60, (255, 255, 255), -1)
                arduino.write(bytes("3", 'utf-8'))
                t_track = False

              elif (xx > 260 and xx < 380 and yy > 180 and yy < 300):

                image = cv2.circle(image, (320, 240), 60, (255, 255, 255), -1)
                #arduino.write(bytes("4", 'utf-8'))
                if(t_track == False):
                    time1 = int(time.time())
                    print(time1)
                    t_track =True

              else:
                arduino.write(bytes("5", 'utf-8'))
                t_track = False

              if(t_track):
                t_gap = int(time.time())-time1
                print(t_gap)

                # add text Labels

                org = (50, 50)

                # fontScale
                fontScale = 1

                # Blue color in BGR
                color = (255, 0, 0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                # Line thickness of 2 px
                thickness = 2

                # Using cv2.putText() method




                if(t_gap==3):
                  image = cv2.circle(image, (320, 240), 60, (0, 0, 255), -1)
                  arduino.write(bytes("4", 'utf-8'))




              image = cv2.circle(image, (xx, yy), 30, (0, 0, 255), -1)

              if(t_gap==0 or t_gap ==1 or t_gap==2):

               image = cv2.putText(image, str((3-t_gap)), (300, 255), cv2.FONT_HERSHEY_SIMPLEX,
                                   2, (255, 0, 0), 2, cv2.LINE_AA)
              #image = cv2.circle(image, (xx, 240), 63, (0, 0, 255), -1)



        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
      arduino.write(bytes("5", 'utf-8'))
      xx = 0
      yy = 720/1.5
    #cv2.imshow('MediaPipe Hands', image)





    scale_percent = 150  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    #print('Resized Dimensions : ', resized.shape)

    resized = cv2.putText(resized,"Miura Research Laboratory", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 0), 2, cv2.LINE_AA)
    resized = cv2.putText(resized,"Boccia Touchless Interface", (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 199), 1, cv2.LINE_AA)
    resized = cv2.putText(resized,"Index Tip Coordinate : "+str(int(xx*1.5))+","+str(720-int(yy*1.5)), (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
                        0.4, (255, 0, 0), 1, cv2.LINE_AA)

    resized = cv2.putText(resized,time.ctime(time.time()),
                          (10, 120), cv2.FONT_HERSHEY_SIMPLEX,
                          0.4, (0, 52, 0), 1, cv2.LINE_AA)
    cv2.imshow("Miura Research Laboratory v0.8", resized)






    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()