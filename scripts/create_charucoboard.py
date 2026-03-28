import cv2


def main():
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    marker = cv2.aruco.generateImageMarker(
        dictionary=dictionary, id=23, sidePixels=200, borderBits=1
    )

    _ = cv2.imwrite("marker23.png", marker)


if __name__ == "__main__":
    main()
