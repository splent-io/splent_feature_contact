"""Signals emitted by the contact feature.

contact stays decoupled from anti-spam: it emits ``contact-submitting`` and any
listener (a captcha provider, a spam filter…) may return False to veto the
submission — mirroring comments' ``comment-submitting``. ``contact-created``
fires after a message is stored, for things like notifications or counters.
"""

from splent_framework.signals.signal_utils import define_signal

contact_submitting = define_signal("contact-submitting", "splent_feature_contact")
contact_created = define_signal("contact-created", "splent_feature_contact")
