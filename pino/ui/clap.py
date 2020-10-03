import argparse as ap

from pino.config import Config


class PinoCli(object):
    def __init__(self):
        self.__parser = ap.ArgumentParser(description="About this program")
        self.__parser.add_argument("--yaml",
                                   "-y",
                                   help="About this argument",
                                   type=str)
        self.__parser.add_argument("--port",
                                   "-p",
                                   help="About this argument",
                                   type=str)
        self.__parser.add_argument("--baudrate",
                                   "-b",
                                   help="About this argument",
                                   type=int)
        self.__parser.add_argument("--dotino",
                                   "-d",
                                   help="About this argument",
                                   type=str)
        self.__parser.add_argument("--timeout",
                                   "-t",
                                   help="About this argument",
                                   type=float)
        self.__parser.add_argument("--warmup",
                                   "-w",
                                   help="About this argument",
                                   type=float)
        self.__parser.add_argument("--arduino",
                                   "-a",
                                   help="About this argument",
                                   type=str)
        self.__args = self.__parser.parse_args()

    def get_config(self) -> Config:
        yml = self.__args.yaml
        return Config(yml)

    def get_port(self) -> str:
        return self.__args.port

    def get_baudrate(self) -> int:
        return self.__args.baudrate

    def get_dotino(self) -> str:
        return self.__args.dotino

    def get_timeout(self) -> float:
        return self.__args.timeout

    def get_warmup(self) -> float:
        return self.__args.warmup

    def get_arduino(self) -> str:
        return self.__args.arduino
