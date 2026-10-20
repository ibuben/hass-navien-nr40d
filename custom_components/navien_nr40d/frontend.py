"""Serve the Lovelace card from the integration itself."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.core import HomeAssistant

from .const import DOMAIN, VERSION

_LOGGER = logging.getLogger(__name__)
_REGISTERED = False
WWW_PATH = Path(__file__).parent / "www"
CARD_FILENAME = "navien-nr40d-card.js"


async def async_register_frontend(hass: HomeAssistant) -> None:
    """Register the static card URL once per Home Assistant instance."""
    global _REGISTERED
    if _REGISTERED or hass.http is None:
        return

    url_path = f"/{DOMAIN}"
    card_url = f"{url_path}/{CARD_FILENAME}?v={VERSION}"
    try:
        from homeassistant.components.http import StaticPathConfig

        await hass.http.async_register_static_paths(
            [StaticPathConfig(url_path, str(WWW_PATH), False)]
        )
    except (ImportError, AttributeError):
        hass.http.register_static_path(url_path, str(WWW_PATH), False)

    add_extra_js_url(hass, card_url)
    _REGISTERED = True
    _LOGGER.debug("Registered Lovelace card %s", card_url)
