import numpy as np
import cv2
import math
import warnings
warnings.simplefilter("ignore", category=RuntimeWarning) #56.57. line throws empty list warningot if there is no edge

def ontrackbar(x): #for rotation
    global rotationMatrix
    rotationMatrix = cv2.getRotationMatrix2D(imageCenter, x, 1.0)#x value the rotation angle
    localResult = cv2.warpAffine(source, rotationMatrix, source.shape[1::-1], flags=cv2.INTER_LINEAR)
    cv2.namedWindow("After", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("After", localResult)
    return localResult

source = cv2.imread('noise.jpg', cv2.IMREAD_COLOR)
image = cv2.medianBlur(source, 5) #noise reduction

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 200, 200, apertureSize=3) #canny edge detection
lines = cv2.HoughLinesP(edges, rho=1, theta=math.pi / 180.0, threshold=100, minLineLength=100, maxLineGap=5) #longest lines
horizontalAngles = [] #for the anges of lines
verticalAngles = []

for line in lines:
    for x1, y1, x2, y2 in line: #x1,x2,y1,y2 the endpoints of the lines
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) # angle with the horizontal line
        if -45 <= angle <= 45: #horizontal lines
            horizontalAngles.append(angle)

        if angle <= -45 or angle >= 45: #vertical lines
            verticalAngles.append(angle)

horizontalAnglesMedian = np.median(horizontalAngles) #measure median for the vertical
verticalAnglesMedian = np.median(verticalAngles) #measure median for the vertical
globalMedian = ((90 - abs(verticalAnglesMedian) + abs(horizontalAnglesMedian)) / 2) #average ° difference without negative sign

if math.isnan(verticalAnglesMedian) is True: #if lines are only from one direction
    globalMedian = horizontalAnglesMedian
if math.isnan(horizontalAnglesMedian) is True:
    globalMedian = verticalAnglesMedian

trackbarOnPoint = globalMedian #good position from the start picture
printPlus = "" #print hack

if verticalAnglesMedian > 0: #rotation direciton. only this important, the vertical has same neg or pos sign
    trackbarOnPoint = 360 - globalMedian # for not to write -24
    globalMedian = -globalMedian # to work counter clockwise too

if trackbarOnPoint < 0: #to not have negative at the third pic too
    trackbarOnPoint = 360 + trackbarOnPoint
    printPlus = ""

print("Rotation angle clockwise", ": "  '{:1.2f}'.format(abs(globalMedian)), '°') #printing nicely

imageCenter = tuple(np.array(image.shape[1::-1]) / 2) #to rotate from the mid point of the pic
rotationMatrix = cv2.getRotationMatrix2D(imageCenter, globalMedian, 1.0) #rotation with the average
result = cv2.warpAffine(image, rotationMatrix, image.shape[1::-1], flags=cv2.INTER_LINEAR)

cv2.namedWindow("Before", cv2.WINDOW_AUTOSIZE) #resize
cv2.imshow("Before", source)
key = cv2.waitKey(0) # exit with keypress
cv2.destroyAllWindows()

cv2.namedWindow("After", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar('Rotate', 'After', int(trackbarOnPoint), 360, ontrackbar) #bar
ontrackbar(globalMedian) #mouse operator callback funcion set to window
key = cv2.waitKey(0)
cv2.destroyAllWindows()

