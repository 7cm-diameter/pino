from typing import Any, Dict

import yaml

Settings = Dict[str, Any]
# Alias for settings
Comport = Settings
Experimental = Settings
Metadata = Settings


class Config(dict):
    def __init__(self, path: str) -> None:
        f = open(path, "r")
        self.__path = path
        d: dict = yaml.safe_load(f)
        [self.__setitem__(item[0], item[1]) for item in d.items()]
        f.close()

    def __missing__(self) -> Settings:
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
