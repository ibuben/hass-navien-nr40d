"""Connection and outdoor sensor binary sensors."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .entity import NavienEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NavienConnectedSensor(coordinator), NavienOutdoorSensorPresence(coordinator)])


class NavienConnectedSensor(NavienEntity, BinarySensorEntity):
    _attr_translation_key = "connected"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "connected")

    @property
    def available(self) -> bool:
        return True

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.connected


class NavienOutdoorSensorPresence(NavienEntity, BinarySensorEntity):
    """The boiler reports an outdoor sensor; its reading is not relayed to the controller."""

    _attr_translation_key = "outdoor_sensor"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator, "outdoor_sensor")

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.data.device is not None

    @property
    def is_on(self) -> bool:
        device = self.coordinator.data.device
        return bool(device and device.outdoor_display == 2)
