from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.nav.nav_registry import register_nav_item
from splent_framework.services.service_locator import register_service

from splent_io.splent_feature_contact.services import ContactService

contact_bp = create_blueprint(__name__)


def init_feature(app):
    from splent_framework.assets.asset_registry import register_asset
    from splent_framework.settings.settings_schema import register_settings

    register_service(app, "ContactService", ContactService)

    # Public contact-form styles, shipped through the asset registry (never
    # inline / CDN) from the feature's OWN assets/css/contact.css.
    register_asset(
        "css", "contact.assets", order=100, subfolder="css", filename="contact.css"
    )

    # Public main-nav entry; surfaces only when the feature is selected.
    register_nav_item(key="contact", label="Contact", href="/contact", order=60)

    # Declarative admin settings — the framework renders the panel and persists
    # the values; routes read them via get_config("contact").
    register_settings(
        "contact",
        "Contact",
        [
            {
                "key": "recipient",
                "type": "text",
                "default": "",
                "label": "Recipient email",
                "help": "Where contact messages are sent.",
            },
            {
                "key": "success_message",
                "type": "text",
                "default": "Thanks — we'll be in touch.",
                "label": "Success message",
            },
        ],
        icon="mail",
    )


def inject_context_vars(app):
    return {}
