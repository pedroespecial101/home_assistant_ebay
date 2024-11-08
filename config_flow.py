"""Config flow for ebay."""
import logging
from .const import DOMAIN
from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.entity import Entity

from yarl import URL
import jwt
import secrets

DATA_JWT_SECRET = "oauth2_jwt_secret"


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle ebay OAuth2 authentication."""

    DOMAIN = DOMAIN
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    async def async_oauth_create_entry(self, data: dict) -> dict:
        """Create an entry for the flow.
        Ok to override if you want to fetch extra info or even add another step.
        """
        data["site_name"] = self.site_name
        return self.async_create_entry(title=self.site_name, data=data)

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow start."""
        if user_input is not None:
            self.site_name = user_input["site_name"]
            return await self.async_step_auth()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("site_name"): str}),
        )
