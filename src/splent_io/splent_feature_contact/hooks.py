"""Template hooks for splent_feature_contact.

Adds an admin "Contact" link to the authenticated sidebar, with a badge showing
how many messages are still unread. The public "Contact" nav entry is declared
via register_nav_item() in __init__.py, not here.
"""

from flask import request, url_for

from splent_framework.hooks.template_hooks import register_template_hook
from splent_framework.services.service_locator import service_proxy


def contact_admin_link():
    active = (
        "active"
        if request.endpoint and request.endpoint.startswith("contact.admin")
        else ""
    )
    pending = 0
    try:
        pending = service_proxy("ContactService").pending_count()
    except Exception:
        pass
    badge = f' <span class="badge bg-danger">{pending}</span>' if pending else ""
    return (
        f'<li class="sidebar-item {active}">'
        f'<a class="sidebar-link" href="{url_for("contact.admin_index")}">'
        '<i class="align-middle" data-feather="mail"></i> '
        f'<span class="align-middle">Contact</span>{badge}</a></li>'
    )


register_template_hook("layout.authenticated_sidebar", contact_admin_link)
