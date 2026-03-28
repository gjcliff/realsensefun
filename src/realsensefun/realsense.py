import pyrealsense2 as rs
import types


class RealSenseD435i:
    pipeline: rs.pipeline | None = None
    profile: rs.pipeline_profile | None = None

    def __enter__(self):
        self.pipeline = rs.pipeline()  # create a pipeline
        config = rs.config()

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        _ = self.pipeline.start(config)  # start streaming

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool:
        if self.pipeline is not None:
            self.pipeline.stop()  # stop streaming
        return False

    @property
    def _pipe(self) -> rs.pipeline:
        if self.pipeline is None:
            raise RuntimeError("")
        return self.pipeline

    def wait_for_frames(self) -> rs.composite_frame:
        frames = self._pipe.wait_for_frames()
        return frames

    def __init__(self): ...
