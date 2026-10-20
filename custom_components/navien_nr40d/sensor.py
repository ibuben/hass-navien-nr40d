"""Diagnostic and measurement sensors."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import NavienCoordinator
from .entity import NavienEntity
from .protocol import decode_outdoor_block_temp


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: NavienCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            NavienRoomTempSensor(coordinator),
            NavienOutdoorTempSensor(coordinator),
            NavienModeSensor(coordinator),
            NavienErrorSensor(coordinator),
        ]
    )


class NavienRoomTempSensor(NavienEntity, SensorEntity):
    _attr_translation_key = "room_temp"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator: NavienCoordinator) -> None:
        super().__init__(coordinator, "room_temp")

    @property
    def available(self) -> bool:
        return super().available and self.status is not None

    @property
    def native_value(self) -> float | None:
        return None if self.status is None else self.status.room_temp


class NavienOutdoorTempSensor(NavienEntity, SensorEntity):
    _attr_translation_key = "outdoor_temp"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator: NavienCoordinator) -> None:
        super().__init__(coordinator, "outdoor_temp")

    @property
    def available(self) -> bool:
        return super().available and self.status is not None

    def _block_temp(self) -> float:
        block = self.coordinator.data.outdoor_block
        return decode_outdoor_block_temp(bytes.fromhex(block)) if block else 0.0

    @property
    def native_value(self) -> float | None:
        status = self.status
        if status is None:
            return None
        # All-zero bytes mean the controller has no reading, not 0 °C outside.
        if status.outdoor_temp != 0:
            return status.outdoor_temp
        block_temp = self._block_temp()
        return block_temp if block_temp != 0 else None

    @property
    def extra_state_attributes(self) -> dict[str, object] | None:
        status = self.status
        if status is None:
            return None
        device = self.coordinator.data.device
        return {
            "status_bytes": status.raw[4:12],
            "status_flag": status.outdoor_display,
            "outdoor_block": self.coordinator.data.outdoor_block,
            "device_display_flag": device.outdoor_display if device else None,
            "device_control_flag": device.outdoor_control if device else None,
            "device_heat_stop_flag": device.outdoor_heat_stop if device else None,
            "status_raw": status.raw,
        }


class NavienModeSensor(NavienEntity, SensorEntity):
    _attr_translation_key = "mode"

    def __init__(self, coordinator: NavienCoordinator) -> None:
        super().__init__(coordinator, "mode")

    @property
    def available(self) -> bool:
        return super().available and self.status is not None

    @property
    def native_value(self) -> str | None:
        return None if self.status is None else self.status.current_mode


class NavienErrorSensor(NavienEntity, SensorEntity):
    _attr_translation_key = "error"
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: NavienCoordinator) -> None:
        super().__init__(coordinator, "error")

    @property
    def available(self) -> bool:
        return super().available and self.status is not None

    @property
    def native_value(self) -> str | None:
        return None if self.status is None else self.status.error_key

    @property
    def extra_state_attributes(self) -> dict[str, int] | None:
        if self.status is None:
            return None
        return {"code": self.status.error_code}
