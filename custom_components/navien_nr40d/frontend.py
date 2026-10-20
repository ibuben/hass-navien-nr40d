"""Serve the Lovelace card and register it as a dashboard resource."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import Event, HomeAssistant

from .const import DOMAIN, VERSION

_LOGGER = logging.getLogger(__name__)
WWW_PATH = Path(__file__).parent / "www"
CARD_FILENAME = "navien-nr40d-card.js"
_STATIC_REGISTERED = False
_STARTED_LISTENER = False


def card_url() -> str:
    return f"/{DOMAIN}/{CARD_FILENAME}?v={VERSION}"


async def async_register_frontend(hass: HomeAssistant) -> None:
    """Expose the JS file and make Lovelace load it."""
    await _async_register_static(hass)
    add_extra_js_url(hass, card_url())
    global _STARTED_LISTENER
    if hass.is_running:
        await _async_register_lovelace_resource(hass)
    elif not _STARTED_LISTENER:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _on_started(hass))
        _STARTED_LISTENER = True


def _on_started(hass: HomeAssistant):
    async def _handle(_event: Event) -> None:
        await _async_register_lovelace_resource(hass)

    return _handle


async def _async_register_static(hass: HomeAssistant) -> None:
    global _STATIC_REGISTERED
    if _STATIC_REGISTERED or hass.http is None:
        return
    url_path = f"/{DOMAIN}"
    try:
        from homeassistant.components.http import StaticPathConfig

        await hass.http.async_register_static_paths(
            [StaticPathConfig(url_path, str(WWW_PATH), False)]
        )
    except (ImportError, AttributeError):
        hass.http.register_static_path(url_path, str(WWW_PATH), False)
    except Exception as err:  # noqa: BLE001
        _LOGGER.debug("Static path already registered: %s", err)
    _STATIC_REGISTERED = True


async def _async_register_lovelace_resource(hass: HomeAssistant) -> None:
    """Add the card to Settings → Dashboards → Resources if possible."""
    lovelace = hass.data.get("lovelace")
    resources = getattr(lovelace, "resources", None)
    if resources is None:
        _LOGGER.debug("Lovelace resources are not available yet")
        return
    try:
        if hasattr(resources, "async_load"):
            await resources.async_load()
        url = card_url()
        base = url.split("?", 1)[0]
        items = list(resources.async_items()) if hasattr(resources, "async_items") else []
        if any(str(item.get("url", "")).split("?", 1)[0] == base for item in items):
            return
        await resources.async_create_item({"res_type": "module", "url": url})
        _LOGGER.info("Registered Lovelace resource %s", url)
    except Exception as err:  # noqa: BLE001
        _LOGGER.warning("Could not auto-register Lovelace resource: %s", err)
