"""Config flow for Navien NR-40D."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_POLL_INTERVAL,
    CONF_PORTS,
    DEFAULT_HOST,
    DEFAULT_NAME,
    DEFAULT_POLL_INTERVAL,
    DEFAULT_PORTS,
    DOMAIN,
)
from .protocol import parse_ports


def _schema(defaults: dict[str, Any] | None = None, *, include_name: bool = True) -> vol.Schema:
    values = defaults or {}
    fields: dict[Any, Any] = {}
    if include_name:
        fields[vol.Optional(CONF_NAME, default=values.get(CONF_NAME, DEFAULT_NAME))] = str
    fields.update(
        {
            vol.Optional(CONF_HOST, default=values.get(CONF_HOST, DEFAULT_HOST)): str,
            vol.Optional(CONF_PORTS, default=values.get(CONF_PORTS, DEFAULT_PORTS)): str,
            vol.Optional(
                CONF_POLL_INTERVAL,
                default=values.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL),
            ): vol.All(vol.Coerce(int), vol.Range(min=10, max=600)),
        }
    )
    return vol.Schema(fields)


class NavienConfigFlow(ConfigFlow, domain=DOMAIN):
    """Set up one local listener for the NR-40D."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            try:
                parse_ports(user_input[CONF_PORTS])
            except ValueError:
                errors[CONF_PORTS] = "invalid_ports"
            else:
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        return self.async_show_form(step_id="user", data_schema=_schema(), errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return NavienOptionsFlow(config_entry)


class NavienOptionsFlow(OptionsFlow):
    """Change listen address, ports, or poll interval."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        current = {**self._config_entry.data, **self._config_entry.options}
        if user_input is not None:
            try:
                parse_ports(user_input[CONF_PORTS])
            except ValueError:
                errors[CONF_PORTS] = "invalid_ports"
            else:
                return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=_schema(current, include_name=False),
            errors=errors,
        )
