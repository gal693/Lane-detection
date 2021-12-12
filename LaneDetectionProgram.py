import cv2
import numpy as np
from sklearn import linear_model


def EdgesDetection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(gaussian, 50, 150)

    return edges


def RegionOfInterest(edgeImage):
    mask = np.zeros(np.shape(edgeImage), np.uint8)
    ignore_mask_color = 255
    roi_corners = np.array([[(90, 350), (530, 350), (400, 225), (310, 225)]])
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    newframe = cv2.bitwise_and(edgeImage, mask)

    return newframe


def HoughTransform(masked_edges):
    # Hough Transform Parameters
    rho = 1
    theta = np.pi / 180
    threshold = 18
    min_length = 20
    max_line = 90

    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_length, max_line)

    return lines


def SeperateLeftRightLines(midOfFrame, lines):
    left_lane_x = []
    left_lane_y = []
    right_lane_x = []
    right_lane_y = []

    #####
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 != x2:
                    grad = (y2 - y1) / (x2 - x1)

                    if y1 < midOfFrame and y2 < midOfFrame:
                        if grad <= 0 and x2 > x1 and y1 > y2:
                            left_lane_x.append([x1])
                            left_lane_x.append([x2])
                            left_lane_y.append([y1])
                            left_lane_y.append([y2])

                        elif grad >= 0 and x2 > x1 and y2 > y1:
                            right_lane_x.append([x1])
                            right_lane_x.append([x2])
                            right_lane_y.append([y1])
                            right_lane_y.append([y2])
                    elif y1 > midOfFrame and y2 > midOfFrame:
                        if grad >= 0 and x2 > x1 and y2 > y1:
                            left_lane_x.append([x1])
                            left_lane_x.append([x2])
                            left_lane_y.append([y1])
                            left_lane_y.append([y2])
                        elif grad <= 0 and x2 > x1 and y1 > y2:
                            right_lane_x.append([x1])
                            right_lane_x.append([x2])
                            right_lane_y.append([y1])
                            right_lane_y.append([y2])

    return left_lane_x, left_lane_y, right_lane_x, right_lane_y


def RansacDrawLane(lines, frame):
    midOfFrame = np.shape(frame)[1] / 2
    left_lane_x, left_lane_y, right_lane_x, right_lane_y = SeperateLeftRightLines(midOfFrame, lines)
    slope_left, slope_right = 0, 0
    x1, y1 = 0, 350
    x2, y2 = 0, 240
    x3, y3 = 0, 240
    x4, y4 = 0, 350

    if len(left_lane_x) > 0 and len(left_lane_x) == len(left_lane_y):
        left_ransac_x = np.array(left_lane_x)
        left_ransac_y = np.array(left_lane_y)

        left_ransac = linear_model.RANSACRegressor(linear_model.LinearRegression())
        left_ransac.fit(left_ransac_x, left_ransac_y)
        slope_left = left_ransac.estimator_.coef_
        intercept_left = left_ransac.estimator_.intercept_

        if slope_left != 0:
            x1 = int((y1 - intercept_left) / slope_left)
            x2 = int((y2 - intercept_left) / slope_left)

            frame = cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 10)

    if len(right_lane_x) > 0 and len(right_lane_x) == len(right_lane_y):
        right_ransac_x = np.array(right_lane_x)
        right_ransac_y = np.array(right_lane_y)

        right_ransac = linear_model.RANSACRegressor()
        right_ransac.fit(right_ransac_x, right_ransac_y)
        slope_right = right_ransac.estimator_.coef_
        intercept_right = right_ransac.estimator_.intercept_

        if slope_right != 0:
            x3 = int((y3 - intercept_right) / slope_right)
            x4 = int((y4 - intercept_right) / slope_right)

            frame = cv2.line(frame, (x3, y3), (x4, y4), (0, 255, 0), 10)

    if slope_right < 0.5 and slope_right > 0 or slope_left >= -0.2 and slope_left < 0:
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, 500)
        fontScale = 0.8
        fontColor = (0, 0, 0)
        lineType = 2

        frame = cv2.putText(frame, "Changing to right lane", (100, 100), font, fontScale, fontColor, lineType,
                            cv2.LINE_AA, False)

    return frame


def imageProcessing(image):
    newframe = image.copy()

    edges = EdgesDetection(newframe)
    newframe = RegionOfInterest(edges)
    lines = HoughTransform(newframe)
    finalResult = RansacDrawLane(lines, image)

    return finalResult


def main():
    capture = cv2.VideoCapture("originalVideo .avi")

    if capture.isOpened():
        width = int(capture.get(3))
        height = int(capture.get(4))
        out = cv2.VideoWriter('out1.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 24, (width, height))

        while capture.isOpened():
            returnFlag, frame = capture.read()

            if returnFlag == True:
                result = imageProcessing(frame)
                cv2.imshow('RealTimeLaneDetection', result)
                out.write(result)

                if cv2.waitKey(10) == 13:
                    break
            else:
                break

    cv2.destroyAllWindows()
    capture.release()


if __name__ == '__main__':
    main()