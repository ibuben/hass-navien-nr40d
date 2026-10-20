"""Away mode switch."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import NavienEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NavienPowerSwitch(coordinator), NavienAwaySwitch(coordinator)])


class NavienPowerSwitch(NavienEntity, SwitchEntity):
    _attr_translation_key = "power"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "power")

    @property
    def available(self) -> bool:
        return super().available and self.status is not None

    @property
    def is_on(self) -> bool:
        status = self.status
        return bool(status and status.power)

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_set_power(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set_power(False)


class NavienAwaySwitch(NavienEntity, SwitchEntity):
    _attr_translation_key = "away"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "away")

    @property
    def available(self) -> bool:
        return super().available and self.status is not None

    @property
    def is_on(self) -> bool:
        status = self.status
        return bool(status and status.current_mode == "away")

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.async_set_away(True)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.async_set_away(False)
