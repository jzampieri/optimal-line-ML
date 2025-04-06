import cv2

def show_track(image_path):
    img = cv2.imread(image_path)
    cv2.imshow("Track", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
