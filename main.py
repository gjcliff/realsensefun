import pyrealsense2 as rs
import cv2
import numpy as np

from realsensefun.realsense import RealSenseD435i, CameraConfig, CameraPreset


def resize_images(
    depth_image: np.ndarray, color_image: np.ndarray
) -> np.ndarray:
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

    with RealSenseD435i(config) as cam:
        assert cam.pipeline is not None
        while True:
            frames = cam.pipeline.wait_for_frames()
            # depth_frame = frames.get_depth_frame()
            # color_frame = frames.get_color_frame()
            ir_frame = frames.get_infrared_frame()

            # if not depth_frame:
            #     continue
            #
            # if not color_frame:
            #     continue
            #
            # depth_image = np.asanyarray(depth_frame.get_data())
            # color_image = np.asanyarray(color_frame.get_data())

            ir_image = np.asanyarray(ir_frame.get_data())
            cv2.imshow("ir_image", ir_image)
            _ = cv2.waitKey(1)

            # If depth and color resolutions are different, resize color image to match depth image for display


if __name__ == "__main__":
    main()
