"""Diagnostics for the NR-40D integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import NavienCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    coordinator: NavienCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = coordinator.data
    device = data.device
    status = data.status
    return {
        "connected": data.connected,
        "peer": data.peer,
        "gateway_id": data.gateway_id,
        "listen_host": coordinator._host,
        "listen_ports": coordinator._ports,
        "poll_interval": coordinator._poll_interval,
        "device": None
        if device is None
        else {
            "model_code": device.model_code,
            "type_code": device.type_code,
            "nation_code": device.nation_code,
            "room_con_ver": device.room_con_ver,
            "main_ver": device.main_ver,
            "main_sub_ver": device.main_sub_ver,
            "room_temp_min": device.room_temp_min,
            "room_temp_max": device.room_temp_max,
            "water_temp_min": device.water_temp_min,
            "water_temp_max": device.water_temp_max,
            "dhw_temp_min": device.dhw_temp_min,
            "dhw_temp_max": device.dhw_temp_max,
            "outdoor_display": device.outdoor_display,
            "outdoor_control": device.outdoor_control,
            "outdoor_heat_stop": device.outdoor_heat_stop,
            "raw": device.raw,
        },
        "status": None
        if status is None
        else {
            "error_code": status.error_code,
            "error_key": status.error_key,
            "current_mode": status.current_mode,
            "power": status.power,
            "heating": status.heating,
            "room_temp": status.room_temp,
            "room_target": status.room_target,
            "water_target": status.water_target,
            "dhw_target": status.dhw_target,
            "outdoor_temp": status.outdoor_temp,
            "outdoor_display": status.outdoor_display,
            "raw": status.raw,
        },
    }
