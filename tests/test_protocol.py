#!/usr/bin/env python3
"""Protocol unit tests that do not need Home Assistant."""

from __future__ import annotations

import datetime
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "custom_components" / "navien_nr40d"))

from protocol import (  # noqa: E402
    Frame,
    FrameParser,
    crc16,
    decode_status,
    parse_ports,
    time_payload,
    whole_degrees,
)


class ProtocolTests(unittest.TestCase):
    def test_roundtrip_frame(self) -> None:
        original = Frame(2, 3, 1, bytes.fromhex("80a036f34cb54204"), 0xCE, bytes([5, 50]))
        encoded = original.encode()
        frames, junk = FrameParser().feed(encoded)
        self.assertEqual(junk, b"")
        self.assertEqual(len(frames), 1)
        frame = frames[0]
        self.assertTrue(frame.crc_ok)
        self.assertEqual(frame.src, 2)
        self.assertEqual(frame.dst, 3)
        self.assertEqual(frame.cmd, 0xCE)
        self.assertEqual(frame.data, bytes([5, 50]))
        self.assertEqual(crc16(encoded[:-2]), int.from_bytes(encoded[-2:], "big"))

    def test_status_decode(self) -> None:
        status = decode_status(bytes.fromhex("01ff000000000000050134326478010a00000003000000000000000001"))
        self.assertEqual(status.error_code, 0)
        self.assertEqual(status.error_key, "ok")
        self.assertEqual(status.current_mode, "room")
        self.assertTrue(status.power)
        self.assertFalse(status.heating)
        self.assertEqual(status.room_temp, 26.0)
        self.assertEqual(status.room_target, 25.0)
        self.assertEqual(status.water_target, 50.0)
        self.assertEqual(status.dhw_target, 60.0)

    def test_error_byte_order(self) -> None:
        status = decode_status(bytes.fromhex("01ff000000000300050134326478010a00000003000000000000000001"))
        self.assertEqual(status.error_code, 3)
        self.assertEqual(status.error_key, "e003")

    def test_whole_degrees(self) -> None:
        self.assertEqual(whole_degrees(25), 50)
        self.assertEqual(whole_degrees(25.4), 50)
        self.assertEqual(whole_degrees("60"), 120)

    def test_time_payload(self) -> None:
        payload = time_payload(datetime.datetime(2026, 10, 20, 11, 30))
        self.assertEqual(list(payload), [26, 10, 20, 3, 11, 30])

    def test_parse_ports(self) -> None:
        self.assertEqual(parse_ports("7000, 21001,21003"), [7000, 21001, 21003])
        with self.assertRaises(ValueError):
            parse_ports("")
        with self.assertRaises(ValueError):
            parse_ports("70000")


if __name__ == "__main__":
    unittest.main()
