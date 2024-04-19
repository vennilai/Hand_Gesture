import cv2
import mediapipe as mp
import pyautogui

from tkinter import messagebox
import time

def run():

    class handDetector():

        def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):

            self.mode = mode
            self.maxHands = maxHands
            self.detectionCon = detectionCon
            self.trackCon = trackCon

            self.mpHands = mp.solutions.hands
            self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.detectionCon, self.trackCon)
            self.mpDraw = mp.solutions.drawing_utils

        def findHands(self, img, draw=True):

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(imgRGB)

            cnt=0

            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:
                    cnt=cnt+1
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
            return img,cnt

        def findPosition(self, img, handNo=0, draw=True):

            lmList = []
            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            return lmList


    wCam, hCam = 640, 480

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector =handDetector(detectionCon=1)

    while True:

        success, img = cap.read()

        img,cnt = detector.findHands(img)

        detector.findPosition(img, draw=False)

        if cnt==1:
            pyautogui.click(button='right')

        elif cnt==2:
            myscreen = pyautogui.screenshot()
            myscreen.save("C:\\Users\\Hello\\\Downloads\\"+str(round(time.time() * 1000))+".png")
            messagebox.showinfo("Detected Two Hands", "Screen shot Captured and Saved in Downloads")

        cv2.imshow("Image", img)
        cv2.waitKey(1000)

run()