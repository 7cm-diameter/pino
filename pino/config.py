from typing import Any, Dict

import yaml

Setting = Dict[str, Any]
# Alias for settings
ComportSetting = Setting
ExperimentalSetting = Setting
MetadataSetting = Setting
PinModeSetting = Dict[int, str]


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
    def comport(self) -> ComportSetting:
        return self["Comport"]

    @property
    def experimental(self) -> ExperimentalSetting:
        return self["Experimental"]

    @property
    def metadata(self) -> MetadataSetting:
        return self["Metadata"]

    @property
    def pinmode(self) -> PinModeSetting:
        return self["PinMode"]
