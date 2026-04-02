import cv2
import numpy as np


class ArucoHelper:
    def __init__(
        self,
        squares_x: int,
        squares_y: int,
        square_length: float,
        marker_length: float,
        dictionary: cv2.aruco.Dictionary,
    ):
        self.charuco_board = cv2.aruco.CharucoBoard(
            (squares_x, squares_y), square_length, marker_length, dictionary
        )
        self.detector = cv2.aruco.CharucoDetector(
            board=self.charuco_board,
            charucoParams=cv2.aruco.CharucoParameters(),
            detectorParams=cv2.aruco.DetectorParameters(),
        )

        self._all_charuco_corners: list[np.ndarray] = []
        self._all_charuco_ids: list[np.ndarray] = []
        self._image_size: tuple[int, int] | None = None
