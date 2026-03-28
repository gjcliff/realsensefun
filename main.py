import pyrealsense2 as rs


def main():
    pipeline = rs.pipeline()  # create a pipeline
    pipeline.start()  # start streaming

    try:
        while True:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame:
                continue

            width, height = depth_frame.get_width(), depth_frame.get_height()
            dist = depth_frame.get_distance(width // 2, height // 2)
            print(
                f"The camera is facing an object {dist:.3f} meters away",
                end="\r",
            )

    finally:
        pipeline.stop()  # stop streaming


if __name__ == "__main__":
    main()
