"""Config flow for ebay beta."""
import logging
import voluptuous as vol
from .const import DOMAIN
from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.core import HomeAssistant, callback


from yarl import URL
import jwt
import secrets

DATA_JWT_SECRET = "oauth2_jwt_secret"


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle ebay beta OAuth2 authentication."""

    DOMAIN = DOMAIN
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
    VERSION = 1

    account_name = None

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    async def async_step_user(self, user_input=None):
        """Handle a flow start."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("account_name"): str,
                })
            )

        self.account_name = user_input["account_name"]
        return await self.async_step_pick_implementation()

    async def async_oauth_create_entry(self, data: dict) -> dict:
        """Create an entry for the flow."""
        if self.account_name:
            data["account_name"] = self.account_name
        else:
            data["account_name"] = "Primary"

        return self.async_create_entry(
            title=f"eBay Beta ({data['account_name']})", 
            data=data
        )
