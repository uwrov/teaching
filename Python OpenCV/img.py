import time
import math
import numpy as np
import cv2
import sys
import thread
import collections


# This program uses the image from a webcam to make an interactive ball bouncing animation. It
# overlays a ball bouncing withing the confines of the window with the image from the webcam, but
# also looks for a neon green line in the image which it extends to a line which the ball can
# interact with.

# To test it out, get somehting kinda light green and longish, and wave it in front of the camera
# while running this.

# Usage:
# 
#     python img.py [cameraNum]

# line = [x, y, dx, dy]
def drawLine(image, line, color, width):
    global oldLineBounds
    refreshPosThresh = 5
    refreshAngThresh = math.pi / 60

    [x, y, dx, dy] = line
    lefty = int(x * -dy / dx + y)
    righty = int((FRAME_WIDTH - x) * dy / dx + y)

    if abs(lefty - oldLineBounds[0] + righty - oldLineBounds[1]) < refreshPosThresh and abs(math.atan2(dy, dx) - oldLineBounds[2]) < refreshAngThresh:
        cv2.line(image, (0, oldLineBounds[0]), (FRAME_WIDTH, oldLineBounds[1]), color, width)
    else:
        oldLineBounds = [lefty, righty, math.atan2(dy, dx)]
        cv2.line(image, (0, lefty), (FRAME_WIDTH, righty), color, width)

# line = [[x1, y1], [x2, y2]] numpy array
# points = [x, y] numpy array
def projection(line, point):
    [p1, p2] = line
    dist = p2 - p1
    normSquared = np.dot(dist, dist)
    t = np.dot(point - p1, dist) / normSquared
    proj = p1 + t * dist

# line = [[x1, y1], [x2, y2]] numpy array
# point = [x, y] numpy array
# first return is distance, second is vector from line to point
def getMinDist(line, point):
    [p1, p2] = line
    dist = p2 - p1
    normSquared = np.dot(dist, dist)
    t = np.dot(point - p1, dist) / normSquared
    proj = p1 + t * dist
    return [np.linalg.norm(point - proj), point - proj]


# line = [[x1, y1], [x2, y2]] numpy array
def testClip(line):
    global ball_vel, ball_pos, oldBallPos
    [p1, p2] = line
    mirrorVec = p2 - p1
    [dist, vec] = getMinDist(line, ball_pos)

    # if dist <= BALL_RADIUS or intersect(line, [ball_pos, oldBallPos]):
    if dist <= BALL_RADIUS:
        vel_rej = ball_vel - np.dot(ball_vel, mirrorVec) * mirrorVec / np.dot(mirrorVec, mirrorVec)
        ball_vel -= vel_rej * 2

        rad_vec = vec / dist * BALL_RADIUS
        adjust = rad_vec - vec
        ball_pos += 2 * adjust


# line = [[x1, y1], [x2, y2]] numpy array
def intersect(line1, line2):
    [a, b] = line1
    [c, d] = line2

    cSign = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
    dSign = (b[0] - a[0]) * (d[1] - b[1]) - (b[1] - a[1]) * (d[0] - b[0])

    if cSign * dSign > 0:
        return False
    else:
        print "int"
        return True

def display_frame():
    while True:
        try:
            i = frame_buffer.popleft()
        except IndexError as e:
            time.sleep(.02)
        else:
            cv2.imshow("window", np.fliplr(i))




# Get command line arguments
if len(sys.argv) <= 1:
    cameraNum = 0
elif len(sys.argv) == 2:
    cameraNum = int(sys.argv[1])

# set options
FRAME_WIDTH = 720 #960 / 2
FRAME_HEIGHT = 405 #540 / 2
FPS = 20
SCALE = 2

frame_buffer = collections.deque()

c = 0
fps_history = 10 * [0]

BALL_RADIUS = 30

    
# Create video capture object
cap = cv2.VideoCapture(cameraNum)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)

ball_pos = np.array([FRAME_WIDTH / 2, FRAME_HEIGHT / 4], dtype=np.float)
ball_vel = np.array([25, 0], dtype=np.float)
ball_acc = np.array([0, 1], dtype=np.float)


line = np.array([0, 0, 0, 1], dtype=np.float)
bounds = np.array([[0, 0, 1, 0], [0, FRAME_HEIGHT, 1, 0], [0, 0, 0, 1], [FRAME_WIDTH, 0, 0, 1]], dtype=np.float)
oldLineBounds = [0, 0, 0]
oldBallPos = np.array([FRAME_WIDTH / 2, FRAME_HEIGHT / 4], dtype=np.float)

# attempt to multithread frame display
try:
   thread.start_new_thread(display_frame, () )
except:
   print "Error: unable to start thread"




##### INTERESTING STUFF BEGINS HERE #####



while (cap.isOpened()):
    start = time.time()
    
    # Capture frame-by-frame
    _, frame = cap.read()

    # convert to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # hsv bounds for the range
    # in this case, we're looking for something in the neon green range (40-70), and keeping the
    # saturation and value from the extremes so we don't get mixed up with random variations of
    # white and black
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([70, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # blur the image to remove noise
    kernel = np.ones((3, 3), np.float32) / 9
    dst = cv2.filter2D(mask, -1, kernel)

    # find blobs
    _, contours, _ = cv2.findContours(dst, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    if len(contours) > 0:
        # sort blobs by size
        blobs = np.argsort(map(cv2.contourArea, contours))

        # find the largest blob (end of the array), but ignore if it's not large enough
        if cv2.contourArea(contours[blobs[-1]]) > 100:
            # fit an ellipse to the blob
            ellipse = cv2.fitEllipse(contours[blobs[-1]])
            (center, axes, orientation) = ellipse
            majoraxis_length = max(axes)
            minoraxis_length = min(axes)
            # look for something that has high eccentricity (ie it's long and skinny)
            eccentricity = np.sqrt(1-(minoraxis_length/majoraxis_length)**2)

            # we're looking for a pole, so high eccentricity only
            if eccentricity > .9:
                # fit a line to the blob
                [dx, dy, x, y] = cv2.fitLine(contours[blobs[-1]], cv2.DIST_L2, 0, 0.01, 0.01)

                # draw the line on the frame
                drawLine(frame, [x, y, dx, dy], (51, 230, 18), 4)
                line = np.array([x, y, dx, dy], dtype=np.float)
                line = np.ndarray.flatten(line)
            else:
                # no blobs suitably line like, so "remove" the line (draw it off screen)
                line = np.array([0, FRAME_HEIGHT * 2, 1, 0], dtype=np.float)
        else:
            # no blobs big enough, so "remove" the line (draw it off screen)
            line = np.array([0, FRAME_HEIGHT * 2, 1, 0], dtype=np.float)
    else:
        # no blobs found, so "remove" the line (draw it off screen)
        line = np.array([0, FRAME_HEIGHT * 2, 1, 0], dtype=np.float)



##### INTERESTING STUFF ENDS HERE #####


    
    # draw the ball
    cv2.circle(frame, tuple(map(int, tuple(ball_pos))), BALL_RADIUS, (0, 0, 255), -1)
    
    # add the frame to the display buffer
    frame_buffer.append(frame)


    # update ball pos and vel
    ball_pos += ball_vel

    # test for clip with line
    testClip(np.array([[line[0], line[1]], [line[0] + line[2], line[1] + line[3]]]))

    oldBallPos = ball_pos


    # update ball if it clips

    if (ball_pos[0] - BALL_RADIUS < 0 or ball_pos[0] + BALL_RADIUS >= FRAME_WIDTH):
        ball_vel *= (-1, 1)
    # if (ball_pos[1] - BALL_RADIUS < 0 or ball_pos[1] + BALL_RADIUS >= FRAME_HEIGHT):
    if (ball_pos[1] + BALL_RADIUS >= FRAME_HEIGHT):
        ball_vel *= (1, -1)


    if (ball_pos[0] - BALL_RADIUS < 0):
        ball_pos += (2 * (BALL_RADIUS - ball_pos[0]), 0)
    # if (ball_pos[1] - BALL_RADIUS < 0):
    #     ball_pos += (0, BALL_RADIUS - ball_pos[1])

    if (ball_pos[0] + BALL_RADIUS >= FRAME_WIDTH):
        offset = 2 * (FRAME_WIDTH - (ball_pos[0] + BALL_RADIUS))
        ball_pos += (offset, 0)
    if (ball_pos[1] + BALL_RADIUS >= FRAME_HEIGHT):
        offset = 2 * (FRAME_HEIGHT - (ball_pos[1] + BALL_RADIUS))
        ball_pos += (0, offset)


    for b in bounds:
        testClip(np.array([[b[0], b[1]], [b[0] + b[2], b[1] + b[3]]]))

    # do physics to it
    ball_vel += ball_acc

    
    # Quit on 'q' press
    press = cv2.waitKey(10);
    if press & 0xFF == ord('q'):
        pass
        
    # whoops, it somehow got way off screen, reset everything
    if ball_pos[0] < 0 or ball_pos[0] > 1000 or ball_pos[1] < 0 or ball_pos[1] > 1000:
        ball_pos = np.array([FRAME_WIDTH / 2, FRAME_HEIGHT / 4], dtype=np.float)
        ball_vel = np.array([25, 0], dtype=np.float)
        ball_acc = np.array([0, 1], dtype=np.float)

    elapsed = time.time() - start
    fps_history[c%10] = 1. / elapsed
    
    # display average fps
    if not (c%10):
        avg = 0
        for i in range(10): avg += fps_history[i]
        avg /= 10
        print int(round(avg)), "fps"
    c += 1

# Release everything
cap.release()
cv2.destroyAllWindows()










