# Lane-detection

1) Edge detection

First of all converted the given frame to gray scale.
Afterwards, noise reduction with cv2.gaussianblur().
For the edges, I used cv2.canny() with the given grayscale gaussian filtered image.

2) Region of interest

I took one frame, scaled it and measured the most significant area of the frame which needed for the lane detection. 
After finding all coordinates of the referred area, I used cv2.fillpoly and a mask to threshold the wanted area out of the frame.

<img width="594" alt="צילום מסך 2021-12-17 ב-13 35 34" src="https://user-images.githubusercontent.com/83302424/146539411-57542c87-ec63-4fb4-b781-e26d1c4688bd.png">


3) Hough transform

I used cv2.houghlinesp on the edge detected region sorted image to get the coordinates of the lines detected in each frame.
 
4) Ransac

The resulted lines from hough transform were not all continuous, some were of the continuous line and some were of the dashed line.
So in order to get continuous lines no matter which lane I got, I used Ransac because I figured I need the get the properties of each line in order to draw a longer
continuous line even if the line is short.

First I separated left lines from right lines by each line gradient.
Afterwards I use Ransac in order to find the correct lines for each frame.
In addition, using the gradient of the resulted lines I found the frames where lane changing occurring.

Inside Ransac I also used cv2.drawline and cv2.puttext In order to modify the original frame, and using cv2.videowriter I inserted it to the result video wanted.


Results:


https://user-images.githubusercontent.com/83302424/146541271-7ac75f81-1ed9-490d-9f13-050bcaa46e8b.mp4

change 1

change 2

change 3

change 4

change 5

change 6

change 7