from datetime import timedelta
import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import DOMAIN, EBAY_QUERIES_SENSOR
from .api import get_ebay_data

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]
    site_name = entry.data["site_name"]

    async def async_update_data():
        try:
            await api.session.async_ensure_token_valid(),
            access_token = api.session.token["access_token"]
            return await get_ebay_data(access_token)
        except Exception as ex:
            raise UpdateFailed(f"Error getting Ebay data: {ex}") from ex

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="ebay",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(minutes=5),
    )
    await coordinator.async_config_entry_first_refresh()

    ebay_entity_list = []

    ebay_entity_list.extend(
        [
            EbayOrders(coordinator, site_name),
        ]
    )

    async_add_entities(ebay_entity_list, True)


class EbayOrders(CoordinatorEntity, SensorEntity):
    """Representation of an eBay Orders sensor."""

    def __init__(self, coordinator, site_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._site_name = site_name
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"eBay Orders ({self._site_name})"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        await self.coordinator.async_request_refresh()
        self._state = self.coordinator.data.get("orders")
