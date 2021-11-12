import os
import sys
from enum import Enum
from subprocess import check_output
from time import sleep
from typing import Iterable, List, Optional

from serial import Serial, SerialException  # type: ignore

from pino.config import PinMode as _PinMode
from pino.config import Setting


class Comport(object):
    def __init__(self):
        from os.path import abspath, dirname, join
        if sys.platform == "win32":
            self.__arduino = os.path.join(os.environ["ProgramFiles(x86)"],
                                          "Arduino", "arduino_debug.exe")
        else:
            self.__arduino = "arduino"
        self.__port = ""
        self.__timeout = None
        self.__baudrate = 115200
        self.__dotino = join(dirname(abspath(__file__)), "proto.ino")
        self.__warmup: Optional[float] = None
        self.__conn = None

    def __del__(self):
        if self.__conn is None:
            return None
        self.__conn.reset_input_buffer()
        self.__conn.reset_output_buffer()
        self.disconnect()

    def apply_settings(self, settings: Setting) -> 'Comport':
        available_settings = [
            "arduino", "port", "baudrate", "timeout", "dotino", "warmup"
        ]
        for k in available_settings:
            if k == "arduino":
                val = settings.get(k)
                if val is not None:
                    self.set_arduino(val)
            if k == "port":
                val = settings.get(k)
                if val is not None:
                    self.set_port(val)
            if k == "baudrate":
                val = settings.get(k)
                if val is not None:
                    self.set_baudrate(val)
            if k == "timeout":
                val = settings.get(k)
                if val is not None:
                    self.set_timeout(val)
            if k == "dotino":
                val = settings.get(k)
                if val is not None:
                    self.set_inofile(val)
            if k == "warmup":
                val = settings.get(k)
                if val is not None:
                    self.set_warmup(val)
        return self

    def set_arduino(self, arduino: str) -> 'Comport':
        self.__arduino = arduino
        return self

    def set_port(self, port: str) -> 'Comport':
        self.__port = port
        return self

    def set_baudrate(self, baudrate: int) -> 'Comport':
        if baudrate not in Serial.BAUDRATES:
            raise SerialException("Given baudrate cannot be used")
        self.__baudrate = baudrate
        return self

    def set_timeout(self, timeout: Optional[float]) -> 'Comport':
        self.__timeout = timeout
        return self

    def set_inofile(self, path: str) -> 'Comport':
        self.__dotino = path
        return self

    def set_warmup(self, duration: float) -> 'Comport':
        self.__warmup = duration
        return self

    def connect(self) -> 'Comport':
        self.__conn = Serial(self.__port,
                             self.__baudrate,
                             timeout=self.__timeout)
        if self.__warmup is not None:
            t: float = self.__warmup
            sleep(t)
        return self

    def disconnect(self):
        """disconnect serial port"""
        try:
            self.__conn.close()
        except SerialException:
            pass
        return None

    @staticmethod
    def __as_command(binary: str, upload: str, port: str) -> str:
        return f"{binary} --upload {upload}, --port {port}"

    def deploy(self) -> 'Comport':
        """Write arduino program to connected board"""
        check_output(self.__as_command(self.__arduino, self.__dotino,
                                       self.__port),
                     shell=True)
        return self

    @property
    def connection(self) -> Optional[Serial]:
        return self.__conn

    @property
    def port(self) -> str:
        return self.__port

    @property
    def baudrate(self) -> int:
        return self.__baudrate

    @property
    def inofile(self) -> str:
        return self.__dotino

    @property
    def warmup(self) -> Optional[float]:
        return self.__warmup

    @property
    def inobin(self) -> str:
        return self.__arduino

    @property
    def timeout(self) -> Optional[float]:
        return self.__timeout

    @staticmethod
    def available_ports() -> None:
        from serial.tools.list_ports import comports
        devs = comports()
        if len(devs) == 0:
            print("No device is connected.")
            return None
        for dev in devs:
            print(dev.device)


def as_bytes(x: int) -> bytes:
    return x.to_bytes(1, "little")


class PinMode(Enum):
    INPUT = b'\x00'
    INPUT_PULLUP = b'\x01'
    OUTPUT = b'\x02'
    SERVO = b'\x03'
    SSINPUT = b'\x04'
    SSINPUT_PULLUP = b'\x05'
    PULSE = b'\x06'


INPUT = PinMode.INPUT
INPUT_PULLUP = PinMode.INPUT_PULLUP
OUTPUT = PinMode.OUTPUT
SSINPUT = PinMode.SSINPUT
SSINPUT_PULLUP = PinMode.SSINPUT_PULLUP
SERVO = PinMode.SERVO


class PinState(Enum):
    LOW = b'\x10'
    HIGH = b'\x11'
    PULSE_ON = b'\x14'
    PULSE_OFF = b'\x15'


LOW = PinState.LOW
HIGH = PinState.HIGH


class Arduino(object):
    def __init__(self, comport: Comport):
        self.__conn = comport.connection

    def set_pinmode(self, pin: int, mode: PinMode) -> None:
        proto = mode.value + as_bytes(pin)
        self.__conn.write(proto)

    def apply_pinmode_settings(self, settings: _PinMode) -> None:
        for pin in settings:
            mode_str = settings[pin]
            if mode_str == "INPUT":
                mode = INPUT
            elif mode_str == "INPUT_PULLUP":
                mode = INPUT_PULLUP
            if mode_str == "SSINPUT":
                mode = SSINPUT
            elif mode_str == "SSINPUT_PULLUP":
                mode = SSINPUT_PULLUP
            elif mode_str == "OUTPUT":
                mode = OUTPUT
            elif mode_str == "SERVO":
                mode = SERVO
            else:
                raise NotImplementedError(
                    f"{mode_str} cannot be used as pin mode.")

            self.set_pinmode(pin, mode)

    def digital_write(self, pin: int, state: PinState) -> None:
        proto = state.value + as_bytes(pin)
        self.__conn.write(proto)

    def multiple_digital_write(self, pins: Iterable[int],
                               states: Iterable[PinState]) -> None:
        [self.digital_write(pin, state) for pin, state in zip(pins, states)]

    def digital_read(self,
                     pin: int,
                     size: int = 0,
                     timeout: Optional[float] = None) -> bytes:
        proto = b'\x10' + as_bytes(pin)
        self.__conn.write(proto)
        return self.__conn.read(size)

    def analog_write(self, pin: int, v: int) -> None:
        proto = b'\x12' + as_bytes(pin) + as_bytes(v)
        self.__conn.write(proto)

    def multiple_analog_write(self, pins: Iterable[int],
                              vs: Iterable[int]) -> None:
        [self.analog_write(pin, v) for pin, v in zip(pins, vs)]

    def analog_read(self,
                    pin: int,
                    size: int = 0,
                    timeout: Optional[float] = None) -> bytes:
        proto = b'\x21' + as_bytes(pin)
        self.__conn.write(proto)
        return self.__conn.read(size)

    def read_until_eol(self) -> Optional[bytes]:
        line: bytes = self.__conn.readline()
        if line == b'':
            return None
        try:
            # to detect cancellation
            # if `readline` is canceled, it returns `\xf*`
            # that can not decode to utf-8
            line.decode("utf-8")
        except UnicodeDecodeError:
            return None
        return line

    def cancel_read(self) -> None:
        self.__conn.cancel_read()
        return None

    def disconnect(self):
        self.__conn.reset_input_buffer()
        self.__conn.reset_output_buffer()
        self.__conn.close()

    def servo_rotate(self, pin: int, angle: int) -> None:
        proto = b'\x13' + as_bytes(pin) + as_bytes(angle)
        self.__conn.write(proto)

    def mulitiple_servo_rotate(self, pins: Iterable[int],
                               angles: Iterable[int]) -> None:
        [self.servo_rotate(pin, angle) for pin, angle in zip(pins, angles)]


class Optuino(Arduino):
    maxidx = 50

    def __init__(self, comport: Comport):
        super().__init__(comport)
        self.__conn = comport.connection
        self.__frequency: List[int] = []
        self.__duration: List[int] = []
        self.__pulsing = False

    @property
    def pulse_settings(self) -> List[str]:
        return [
            f"{i}: Frequency - {freq}  Duration - {dur}"
            for (i, (freq,
                     dur)) in enumerate(zip(self.__frequency, self.__duration))
        ]

    @property
    def pulse_frequency(self) -> List[int]:
        return self.__frequency

    @property
    def pulse_duration(self) -> List[int]:
        return self.__duration

    @property
    def pulsing(self) -> bool:
        return self.__pulsing

    def set_pulse_params(self, setting_idx: int, freq: int,
                         duration: int) -> None:
        if setting_idx >= self.maxidx:
            IndexError(f"idx must be lower than {self.maxidx}")
        proto = PinMode.PULSE.value \
            + as_bytes(setting_idx) + as_bytes(freq) + as_bytes(duration)
        self.__conn.write(proto)
        self.__frequency.append(freq)
        self.__duration.append(duration)

    # `pulse_on` blocks other arduino functions until `pulse_off` is called
    # python's processes are not blocked
    def pulse_on(self, pin: int, idx: int) -> None:
        if self.pulsing:
            return None
        proto = PinState.PULSE_ON.value + as_bytes(pin) + as_bytes(idx)
        self.__conn.write(proto)
        self.__pulsing = True

    def pulse_off(self) -> None:
        if not self.pulsing:
            return None
        proto = PinState.PULSE_OFF.value
        self.__conn.write(proto)
        self.__pulsing = False
