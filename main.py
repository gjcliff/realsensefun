import cv2
import numpy as np

from realsensefun.aruco import ArucoHelper
from realsensefun.realsense import CameraConfig, CameraPreset, RealSenseD435i


def resize_images(depth_image: np.ndarray, color_image: np.ndarray) -> np.ndarray:
    depth_colormap = cv2.applyColorMap(
        cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET
    )
    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(
            color_image,
            dsize=(depth_colormap_dim[1], depth_colormap_dim[0]),
            interpolation=cv2.INTER_AREA,
        )
        images = np.hstack((resized_color_image, depth_colormap))
    else:
        images = np.hstack((color_image, depth_colormap))

    return images


def main():
    config = CameraConfig(
        preset=CameraPreset.IR_LEFT,
        width=848,
        height=480,
        fps=30,
        emitter_enabled=False,
    )

    helper = ArucoHelper(
        squares_x=7,
        squares_y=5,
        square_length=0.032,
        marker_length=0.0237,
        dictionary=cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250),
    )

    with RealSenseD435i(config) as cam:
        assert cam.pipeline is not None
        while True:
            frames = cam.pipeline.wait_for_frames()
            ir_frame = frames.get_infrared_frame()
            ir_image = np.asanyarray(ir_frame.get_data())

            display = ir_image.copy()

            charuco_corners, charuco_ids, marker_corners, marker_ids = (
                helper.detector.detectBoard(ir_image)
            )

            if marker_ids is not None:
                cv2.aruco.drawDetectedMarkers(display, marker_corners, marker_ids)

            if charuco_ids is not None:
                cv2.aruco.drawDetectedCornersCharuco(
                    display, charuco_corners, charuco_ids
                )

            _ = cv2.putText(
                display,
                f"frames: {len(helper._all_charuco_corners)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                255,
                2,
            )
            cv2.imshow("ir_image", display)

            key = cv2.waitKey(1)

            if key == ord("c"):
                accepted = helper.process_frame(ir_image)
                print(
                    f"{'accepted' if accepted else 'rejected'}  total: {len(helper._all_charuco_corners)}"
                )

            if key == ord("q"):
                break

            # If depth and color resolutions are different, resize color image to match depth image for display


if __name__ == "__main__":
    main()
