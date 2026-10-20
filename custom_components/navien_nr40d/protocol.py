"""NR-40D local TCP frame format and status decoding.

Frame: F7 | src | dst | proto | gateway_id[8] | cmd | len(LE16) | data | crc16(BE)
CRC is CRC-16/BUYPASS (poly 0x8005, init 0, no reflection) over everything before it.
"""

from __future__ import annotations

import datetime
import struct
from dataclasses import dataclass

try:
    from .const import (
        CURRENT_MODES,
        DHW_TEMP_MAX,
        DHW_TEMP_MIN,
        ERROR_KEYS,
        MODE_POWER_OFF,
        ROOM_TEMP_MAX,
        ROOM_TEMP_MIN,
        WATER_TEMP_MAX,
        WATER_TEMP_MIN,
    )
except ImportError:  # unittest without the Home Assistant package
    from const import (
        CURRENT_MODES,
        DHW_TEMP_MAX,
        DHW_TEMP_MIN,
        ERROR_KEYS,
        MODE_POWER_OFF,
        ROOM_TEMP_MAX,
        ROOM_TEMP_MIN,
        WATER_TEMP_MAX,
        WATER_TEMP_MIN,
    )

HEADER = 0xF7
HEADER_LEN = 15


def crc16(data: bytes) -> int:
    crc = 0
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x8005) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def whole_degrees(value: float | str) -> int:
    """Setpoints travel in 0.5 °C units; the NR-40D only accepts whole degrees."""
    return int(round(float(value))) * 2


def time_payload(now: datetime.datetime | None = None) -> bytes:
    moment = now or datetime.datetime.now()
    dow = (moment.weekday() + 1) % 7 + 1
    return bytes([moment.year - 2000, moment.month, moment.day, dow, moment.hour, moment.minute])


def parse_ports(value: str) -> list[int]:
    ports = [int(part.strip()) for part in value.split(",") if part.strip()]
    if not ports:
        raise ValueError("at least one TCP port is required")
    for port in ports:
        if not 1 <= port <= 65535:
            raise ValueError(f"invalid TCP port: {port}")
    return ports


@dataclass
class DeviceCaps:
    model_code: int = 0
    type_code: int = 0
    nation_code: int = 0
    room_con_ver: int = 0
    main_ver: int = 0
    main_sub_ver: int = 0
    room_temp_min: float = ROOM_TEMP_MIN
    room_temp_max: float = ROOM_TEMP_MAX
    water_temp_min: float = WATER_TEMP_MIN
    water_temp_max: float = WATER_TEMP_MAX
    dhw_temp_min: float = DHW_TEMP_MIN
    dhw_temp_max: float = DHW_TEMP_MAX
    raw: str = ""


@dataclass
class NavienStatus:
    error_code: int = 0
    error_key: str = "ok"
    current_mode: str = "off"
    current_mode_raw: int = MODE_POWER_OFF
    power: bool = False
    heating: bool = False
    operate_mode_raw: int = 0
    room_temp: float = 0.0
    room_target: float = 21.0
    water_target: float = 50.0
    dhw_target: float = 50.0
    heat_level: int = 0
    quick_hot_water: int = 0
    raw: str = ""


@dataclass
class NavienData:
    connected: bool = False
    peer: str | None = None
    gateway_id: str | None = None
    device: DeviceCaps | None = None
    status: NavienStatus | None = None


class Frame:
    def __init__(self, src: int, dst: int, proto: int, gw: bytes, cmd: int, data: bytes = b"") -> None:
        self.src = src
        self.dst = dst
        self.proto = proto
        self.gw = bytes(gw)
        self.cmd = cmd
        self.data = bytes(data)
        self.crc_ok = True
        self.raw = b""

    def encode(self) -> bytes:
        body = bytes([HEADER, self.src, self.dst, self.proto]) + self.gw
        body += bytes([self.cmd]) + struct.pack("<H", len(self.data)) + self.data
        body += struct.pack(">H", crc16(body))
        return body

    def __repr__(self) -> str:
        return (
            f"Frame(src={self.src} dst={self.dst} proto={self.proto} gw={self.gw.hex()} "
            f"cmd=0x{self.cmd:02x} len={len(self.data)} data={self.data.hex(' ')})"
        )


class FrameParser:
    """Incremental parser; returns (frames, junk) for each chunk."""

    def __init__(self) -> None:
        self.buf = bytearray()

    def feed(self, chunk: bytes) -> tuple[list[Frame], bytes]:
        self.buf += chunk
        frames: list[Frame] = []
        junk = bytearray()
        while self.buf:
            if self.buf[0] != HEADER:
                junk.append(self.buf.pop(0))
                continue
            if len(self.buf) < HEADER_LEN:
                break
            length = self.buf[13] | (self.buf[14] << 8)
            total = HEADER_LEN + length + 2
            if len(self.buf) < total:
                break
            raw = bytes(self.buf[:total])
            del self.buf[:total]
            ok = crc16(raw[:-2]) == struct.unpack(">H", raw[-2:])[0]
            frame = Frame(raw[1], raw[2], raw[3], raw[4:12], raw[12], raw[15 : 15 + length])
            frame.crc_ok = ok
            frame.raw = raw
            frames.append(frame)
        return frames, bytes(junk)


def decode_device(data: bytes) -> DeviceCaps:
    payload = data.ljust(33, b"\x00")
    return DeviceCaps(
        model_code=payload[0],
        type_code=payload[1],
        nation_code=payload[3],
        room_con_ver=payload[5],
        main_ver=payload[6],
        main_sub_ver=payload[7],
        room_temp_min=payload[11] / 2,
        room_temp_max=payload[12] / 2,
        water_temp_min=payload[14] / 2,
        water_temp_max=payload[15] / 2,
        dhw_temp_min=payload[21] / 2,
        dhw_temp_max=payload[22] / 2,
        raw=payload.hex(),
    )


def decode_status(data: bytes) -> NavienStatus:
    payload = data.ljust(29, b"\x00")
    error = (payload[7] << 8) | payload[6]
    mode = payload[8]
    return NavienStatus(
        error_code=error,
        error_key=ERROR_KEYS.get(error, "unknown"),
        current_mode=CURRENT_MODES.get(mode, str(mode)),
        current_mode_raw=mode,
        power=mode != MODE_POWER_OFF,
        heating=payload[9] == 2,
        operate_mode_raw=payload[9],
        room_temp=payload[10] / 2,
        room_target=payload[11] / 2,
        water_target=payload[12] / 2,
        dhw_target=payload[13] / 2,
        heat_level=payload[19],
        quick_hot_water=payload[28],
        raw=payload.hex(),
    )
