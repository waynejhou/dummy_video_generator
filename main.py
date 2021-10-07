import cv2
import numpy as np
from tqdm import tqdm
import random


FPS = 30
TOTAL_SEC = 300
OUT_SIZE = (1080, 1920)
OUT_PATH = "dummy video port.mp4"
VID_4CC = cv2.VideoWriter_fourcc(*'mp4v')
VID_BG = (255, 255, 255)
VID_FRAME_TEXT_SCALE = 2
VID_FRAME_TEXT_COLOR = (0, 0, 0)
VID_FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
VID_FONT_THICKNESS = 2

BALL_LENGTH = random.randint(100, 300)
BALL_SIZE = (BALL_LENGTH, BALL_LENGTH)
BALL_POS = [random.randint(0, OUT_SIZE[0]-BALL_SIZE[0]),
            random.randint(0, OUT_SIZE[1]-BALL_SIZE[1])]
BALL_SPEED = random.randint(5, 15)
BALL_VELOCITY = [(random.randint(0, 1)*2-1)*BALL_SPEED,
                 (random.randint(0, 1)*2-1)*BALL_SPEED]
BALL_COLOR = (0, 255, 0)

vWritter = cv2.VideoWriter(OUT_PATH, VID_4CC, FPS, OUT_SIZE)


total_frame = FPS * TOTAL_SEC

for i in tqdm(range(total_frame)):
    img = np.zeros((OUT_SIZE[1], OUT_SIZE[0], 3), np.uint8)
    img[:] = cv2.rectangle(img, (0, 0), OUT_SIZE, VID_BG, -1)

    img[:] = cv2.rectangle(img, BALL_POS, (BALL_POS[0] +
                           BALL_SIZE[0], BALL_POS[1]+BALL_SIZE[1]), BALL_COLOR, -1)

    BALL_POS[0] = min(max(BALL_POS[0]+BALL_VELOCITY[0], 0),
                      OUT_SIZE[0]-BALL_SIZE[0])
    BALL_POS[1] = min(max(BALL_POS[1]+BALL_VELOCITY[1], 0),
                      OUT_SIZE[1]-BALL_SIZE[1])

    if BALL_POS[0] == 0 or BALL_POS[0] + BALL_SIZE[0] == OUT_SIZE[0]:
        BALL_VELOCITY[0] = -BALL_VELOCITY[0]

    if BALL_POS[1] == 0 or BALL_POS[1] + BALL_SIZE[1] == OUT_SIZE[1]:
        BALL_VELOCITY[1] = -BALL_VELOCITY[1]

    fpsText = f"fps: {FPS}"
    (_, fps_text_hei), _ = cv2.getTextSize(
        fpsText, VID_FONT_FACE, VID_FRAME_TEXT_SCALE, VID_FONT_THICKNESS)
    fps_text_hei += 10
    img[:] = cv2.putText(img, fpsText, (10, fps_text_hei), VID_FONT_FACE,
                         VID_FRAME_TEXT_SCALE, VID_FRAME_TEXT_COLOR, VID_FONT_THICKNESS, cv2.LINE_AA)

    frame = i+1
    frameText = f"frame: {frame}"
    (_, frame_text_hei), _ = cv2.getTextSize(frameText,
                                             VID_FONT_FACE, VID_FRAME_TEXT_SCALE, VID_FONT_THICKNESS)
    frame_text_hei += 10
    img[:] = cv2.putText(img, frameText, (10, fps_text_hei + frame_text_hei), VID_FONT_FACE,
                         VID_FRAME_TEXT_SCALE, VID_FRAME_TEXT_COLOR, VID_FONT_THICKNESS, cv2.LINE_AA)

    sec = (i+1) / FPS
    secText = f"sec: {sec:.3f}"
    (_, sec_hei), _ = cv2.getTextSize(
        secText, VID_FONT_FACE, VID_FRAME_TEXT_SCALE, VID_FONT_THICKNESS)
    sec_hei += 10
    img[:] = cv2.putText(img, secText, (10, sec_hei+fps_text_hei+frame_text_hei), VID_FONT_FACE,
                         VID_FRAME_TEXT_SCALE, VID_FRAME_TEXT_COLOR, VID_FONT_THICKNESS, cv2.LINE_AA)

    percent = (i+1)/total_frame
    percentText = f"{percent:.3%}"
    (_, percent_hei), _ = cv2.getTextSize(percentText,
                                          VID_FONT_FACE, VID_FRAME_TEXT_SCALE, VID_FONT_THICKNESS)
    percent_hei += 10
    img[:] = cv2.putText(img, percentText, (10, percent_hei+sec_hei+fps_text_hei+frame_text_hei),
                         VID_FONT_FACE, VID_FRAME_TEXT_SCALE, VID_FRAME_TEXT_COLOR, VID_FONT_THICKNESS, cv2.LINE_AA)

    vWritter.write(img)

vWritter.release()
