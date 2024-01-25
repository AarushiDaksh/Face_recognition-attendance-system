import cv2
cam_port = 0
cam = cv2.VideoCapture(cam_port)
inp = input('Enter person name')
while True: 
    result, image = cam.read()
    cv2.imshow(inp, image)

    key = cv2.waitKey(1)

    if key == 13:
        cv2.imwrite(inp + ".png", image)
        print("Image taken")
        break
cam.release()
cv2.destroyAllWindows()
