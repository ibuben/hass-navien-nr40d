"""Climate entity for room heating."""

from __future__ import annotations

from typing import Any

from homeassistant.components.climate import (
    PRESET_AWAY,
    PRESET_NONE,
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, PRECISION_HALVES, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ROOM_TEMP_MAX, ROOM_TEMP_MIN
from .entity import NavienEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([NavienClimate(hass.data[DOMAIN][entry.entry_id])])


class NavienClimate(NavienEntity, ClimateEntity):
    """Room thermostat. Changing the target switches the boiler to room mode."""

    _attr_name = None
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]
    _attr_preset_modes = [PRESET_NONE, PRESET_AWAY]
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 1
    _attr_precision = PRECISION_HALVES
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.PRESET_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )

    @property
    def available(self) -> bool:
        return super().available and self.status is not None

    @property
    def hvac_mode(self) -> HVACMode:
        status = self.status
        return HVACMode.HEAT if status and status.power else HVACMode.OFF

    @property
    def hvac_action(self) -> HVACAction:
        status = self.status
        if not status or not status.power:
            return HVACAction.OFF
        return HVACAction.HEATING if status.heating else HVACAction.IDLE

    @property
    def native_current_temperature(self) -> float | None:
        return None if self.status is None else self.status.room_temp

    @property
    def native_target_temperature(self) -> float | None:
        return None if self.status is None else self.status.room_target

    @property
    def min_temp(self) -> float:
        device = self.coordinator.data.device
        return device.room_temp_min if device else ROOM_TEMP_MIN

    @property
    def max_temp(self) -> float:
        device = self.coordinator.data.device
        return device.room_temp_max if device else ROOM_TEMP_MAX

    @property
    def preset_mode(self) -> str:
        status = self.status
        return PRESET_AWAY if status and status.current_mode == "away" else PRESET_NONE

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        await self.coordinator.async_set_power(hvac_mode != HVACMode.OFF)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None:
            await self.coordinator.async_set_room_temp(temperature)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        await self.coordinator.async_set_away(preset_mode == PRESET_AWAY)
