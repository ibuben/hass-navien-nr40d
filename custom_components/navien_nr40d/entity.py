"""Shared entity helpers."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import NavienCoordinator
from .protocol import NavienStatus


class NavienEntity(CoordinatorEntity[NavienCoordinator]):
    """Base entity attached to the single NR-40D device."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: NavienCoordinator, key: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"

    @property
    def device_info(self) -> DeviceInfo:
        return self.coordinator.device_info

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.data.connected

    @property
    def status(self) -> NavienStatus | None:
        return self.coordinator.data.status
