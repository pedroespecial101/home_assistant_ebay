"""The eBay Beta integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = config_entry_oauth2_flow.OAUTH2_CLIENT_CONFIG_SCHEMA(DOMAIN)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the eBay Beta component."""
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_IMPORT},
            data=config[DOMAIN],
        )
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up eBay Beta from a config entry."""
    implementation = await config_entry_oauth2_flow.async_get_config_entry_implementation(
        hass, entry
    )

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)

    # If using a custom session class
    # session = MyCustomOAuth2Session(hass, config_entry, implementation)

    hass.data[DOMAIN][entry.entry_id] = session

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
