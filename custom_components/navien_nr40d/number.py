"""Number entities for water and DHW setpoints."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DHW_TEMP_MAX,
    DHW_TEMP_MIN,
    DOMAIN,
    WATER_TEMP_MAX,
    WATER_TEMP_MIN,
)
from .coordinator import NavienCoordinator
from .entity import NavienEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: NavienCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            NavienWaterTempNumber(coordinator),
            NavienDhwTempNumber(coordinator),
        ]
    )


class NavienNumber(NavienEntity, NumberEntity):
    _attr_native_step = 1
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_mode = NumberMode.SLIDER

    @property
    def available(self) -> bool:
        return super().available and self.status is not None


class NavienWaterTempNumber(NavienNumber):
    _attr_translation_key = "water_temp"

    def __init__(self, coordinator: NavienCoordinator) -> None:
        super().__init__(coordinator, "water_temp")

    @property
    def native_min_value(self) -> float:
        device = self.coordinator.data.device
        return device.water_temp_min if device else WATER_TEMP_MIN

    @property
    def native_max_value(self) -> float:
        device = self.coordinator.data.device
        return device.water_temp_max if device else WATER_TEMP_MAX

    @property
    def native_value(self) -> float | None:
        return None if self.status is None else self.status.water_target

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_set_water_temp(value)


class NavienDhwTempNumber(NavienNumber):
    _attr_translation_key = "dhw_temp"

    def __init__(self, coordinator: NavienCoordinator) -> None:
        super().__init__(coordinator, "dhw_temp")

    @property
    def native_min_value(self) -> float:
        device = self.coordinator.data.device
        return device.dhw_temp_min if device else DHW_TEMP_MIN

    @property
    def native_max_value(self) -> float:
        device = self.coordinator.data.device
        return device.dhw_temp_max if device else DHW_TEMP_MAX

    @property
    def native_value(self) -> float | None:
        return None if self.status is None else self.status.dhw_target

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.async_set_dhw_temp(value)
