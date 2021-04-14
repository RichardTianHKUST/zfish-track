import json
from dataclasses import dataclass, asdict, replace
from pathlib import Path
from typing import Optional

from ._io import get_file

config_suffix = '_config.json'
angles_suffix = '_angles.csv'
points_suffix = '_points.csv'
methods = ['binary']


@dataclass
class TrackingConfiguration:
    video_path: str
    method: str = 'binary'
    roi: Optional[tuple] = None
    interval: Optional[tuple] = None
    params: Optional[dict] = None

    def __post_init__(self):
        self.video_path = Path(self.video_path).absolute().as_posix()
        assert self.method in methods
        if self.roi is not None:
            self.roi = tuple(map(int, self.roi))
            assert len(self.roi) == 4
        if self.interval is not None:
            self.interval = tuple(self.interval)
            assert len(self.interval) == 2

    def save(self, video_path=None, verbose=0):
        if video_path is not None:
            return replace(self, video_path=video_path).save(verbose=verbose)

        json_path = get_file(self.video_path, '_' + str(tuple(self.interval)) + config_suffix) \
            if isinstance(self.interval, tuple) \
            else get_file(self.video_path, config_suffix)

        with open(json_path, 'w') as f:
            json.dump(asdict(self), f)

        if verbose:
            print(f'Configuration saved to {json_path}')

    @staticmethod
    def load(json_path):
        with open(json_path, 'r') as f:
            return TrackingConfiguration(**json.load(f))
