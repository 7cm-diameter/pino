from typing import Any, Dict, List, Optional, Tuple

import yaml

Setting = Dict[str, Any]
# Alias for settings
ExperimentalSetting = Setting
MetadataSetting = Setting


class ComportSetting(Dict[str, Any]):
    """Interface to configure `Comport` by yaml file"""
    available_attr = [
        "arduino", "port", "baudrate", "timeout", "dotino", "warmup"
    ]

    def __init__(self, setting: Optional[List[Tuple[str, Any]]] = None):
        """Instantiate ComportSetting

        Parameters
        ----------
        setting: Optional[List[Tuple[str, Any]]] = None
            List of pair of attribute names and values.
        """
        from os.path import abspath, dirname, join
        super().__init__()
        self["arduino"] = "arduino"
        self["baudrate"] = 115200
        self["dotino"] = join(dirname(abspath(__file__)), "proto.ino")
        if setting is None:
            return None
        for k, v in setting:
            self[k] = v

    def __setitem__(self, key: str, value: Any):
        if key not in self.available_attr:
            raise ValueError(f"{key} is not allowed as comport setting.")
        if key == "arduino":
            if not isinstance(value, str):
                raise ValueError("`arduino` must be str")
        elif key == "port":
            if not isinstance(value, str):
                raise ValueError("`port` must be str")
        elif key == "baudrate":
            if not isinstance(value, int):
                raise ValueError("`baudrate` must be int")
        elif key == "timeout":
            if not isinstance(value, float):
                raise ValueError("`timeout` must be float")
        elif key == "dotino":
            if not isinstance(value, str):
                raise ValueError("`dotino` must be str")
        elif key == "warmup":
            if not isinstance(value, float):
                raise ValueError("`warmup` must be float")
        super().__setitem__(key, value)


class PinModeSetting(Dict[int, str]):
    """Interface to configure pin mode by yaml file"""
    available_modes = [
        "INPUT", "INPUT_PULLUP", "OUTPUT", "SERVO", "SSINPUT",
        "SSINPUT_PULLUP", "PULSE"
    ]

    def __init__(self, setting: Optional[List[Tuple[int, str]]] = None):
        """Instantiate PinModeSetting

        Parameters
        ----------
        setting: Optional[List[Tuple[str, Any]]] = None
            List of pair of attribute names and values.
        """
        super().__init__()
        if setting is None:
            return None
        for k, v in setting:
            self[k] = v

    def __setitem__(self, key: int, value: str):
        if not isinstance(key, int):
            raise ValueError("key must be int.")
        if value not in self.available_modes:
            raise ValueError(f"{value} is not allowed as pin mode.")
        super().__setitem__(key, value)


class Config(dict):
    """Read the yaml file and generate `ComportSetting` and `PinModeSetting`"""
    def __init__(self, path: str) -> None:
        """Instantiate Config

        Parameters
        ----------
        path: str
            Path to a yaml file.
        """
        f = open(path, "r")
        self.__path = path
        d: dict = yaml.safe_load(f)
        [self.__setitem__(item[0], item[1]) for item in d.items()]
        f.close()

    def __missing__(self) -> Setting:
        return dict()

    @property
    def comport(self) -> ComportSetting:
        """Return `ComportSetting` generated based on the yaml file

        Returns
        -------
        comport: ComportSetting
            Instance of `ComportSetting` generated based on the yaml file
        """
        cms = ComportSetting()
        for k, v in self["Comport"].items():
            cms[k] = v
        return cms

    @property
    def experimental(self) -> ExperimentalSetting:
        return self["Experimental"]

    @property
    def metadata(self) -> MetadataSetting:
        return self["Metadata"]

    # @property
    # def pinmode(self) -> PinModeSetting:
    #     return self["PinMode"]
    @property
    def pinmode(self) -> PinModeSetting:
        """Return `PinModeSetting` generated based on the yaml file

        Returns
        -------
        pinmode: PinModeSetting
            Instance of `PinModeSetting` generated based on the yaml file
        """
        pms = PinModeSetting()
        for k, v in self["PinMode"].items():
            pms[k] = v
        return pms
