import pyrealsense2 as rs
import types

from dataclasses import dataclass, field
from enum import Enum, auto


class CameraPreset(Enum):
    DEPTH_AND_COLOR = auto()
    IR_LEFT = auto()
    IR_STEREO = auto()
    IR_AND_DEPTH = auto()


@dataclass
class CameraConfig:
    preset: CameraPreset = CameraPreset.IR_LEFT
    width: int = 848
    height: int = 480
    fps: int = 30
    emitter_enabled: bool = False


class RealSenseD435i:
    pipeline: rs.pipeline | None = None
    profile: rs.pipeline_profile | None = None

    def __init__(self, config: CameraConfig | None = None):
        if config is None:
            config = CameraConfig()

        self._cfg = config

    def __enter__(self):
        self.pipeline = rs.pipeline()  # create a pipeline
        config = rs.config()

        c = self._cfg
        match c.preset:
            case CameraPreset.DEPTH_AND_COLOR:
                config.enable_stream(
                    rs.stream.depth, c.width, c.height, rs.format.z16, c.fps
                )
                config.enable_stream(
                    rs.stream.color, c.width, c.height, rs.format.bgr8, c.fps
                )
            case CameraPreset.IR_LEFT:
                config.enable_stream(
                    rs.stream.infrared,
                    1,
                    c.width,
                    c.height,
                    rs.format.y8,
                    c.fps,
                )
            case CameraPreset.IR_STEREO:
                config.enable_stream(
                    rs.stream.infrared,
                    1,
                    c.width,
                    c.height,
                    rs.format.y8,
                    c.fps,
                )
                config.enable_stream(
                    rs.stream.infrared,
                    2,
                    c.width,
                    c.height,
                    rs.format.y8,
                    c.fps,
                )
            case CameraPreset.IR_AND_DEPTH:
                config.enable_stream(
                    rs.stream.infrared,
                    1,
                    c.width,
                    c.height,
                    rs.format.y8,
                    c.fps,
                )
                config.enable_stream(
                    rs.stream.depth, c.width, c.height, rs.format.z16, c.fps
                )

        self.profile = self.pipeline.start(config)  # start streaming

        if not c.emitter_enabled:
            sensor = self.profile.get_device().query_sensors()[0]
            sensor.set_option(rs.option.emitter_enabled, 0)

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
