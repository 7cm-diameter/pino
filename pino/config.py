from typing import Any, Dict

import yaml

Setting = Dict[str, Any]
# Alias for settings
Comport = Setting
Experimental = Setting
Metadata = Setting
PinMode = Dict[int, str]


class Config(dict):
    def __init__(self, path: str) -> None:
        f = open(path, "r")
        self.__path = path
        d: dict = yaml.safe_load(f)
        [self.__setitem__(item[0], item[1]) for item in d.items()]
        f.close()

    def __missing__(self) -> Setting:
        return dict()

    @property
    def comport(self) -> Comport:
        return self["Comport"]

    @property
    def experimental(self) -> Experimental:
        return self["Experimental"]

    @property
    def metadata(self) -> Metadata:
        return self["Metadata"]

    @property
    def pinmode(self) -> PinMode:
        return self["PinMode"]
