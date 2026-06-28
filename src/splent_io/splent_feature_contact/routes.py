from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from splent_io.splent_feature_contact import contact_bp
from splent_io.splent_feature_contact.signals import (
    contact_created,
    contact_submitting,
)
from splent_framework.services.service_locator import service_proxy
from splent_framework.settings.settings_schema import get_config

contact_service = service_proxy("ContactService")


# =====================================================================
# PUBLIC — the contact form
# =====================================================================
@contact_bp.route("/contact", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("contact/index.html")

    # Let any listener (a captcha provider, a spam filter…) veto the submission.
    # contact knows nothing about captchas — they connect to this signal.
    results = contact_submitting.send(
        None, form=request.form, remoteip=request.remote_addr
    )
    if any(value is False for _, value in results):
        flash("Spam check failed — please try again.", "danger")
        return redirect(url_for("contact.index"))

    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    subject = (request.form.get("subject") or "").strip()
    message = (request.form.get("message") or "").strip()

    if not (name and email and message):
        flash("Name, email and message are required.", "danger")
        return redirect(url_for("contact.index"))

    contact_message = contact_service.create_message(
        name=name, email=email, subject=subject, message=message
    )

    # Notify the configured recipient. The message is already saved, so a mail
    # failure must not lose it — wrap in try/except and still flash success.
    mail = service_proxy("MailService")
    recipient = get_config("contact").get("recipient") or ""
    if not recipient:
        try:
            recipient = mail.from_address()
        except Exception:
            recipient = None

    body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}\n"
    if recipient:
        try:
            mail.send(
                to=recipient,
                subject="[Contact] " + (subject or "(no subject)"),
                body=body,
                reply_to=email,
            )
        except Exception:
            pass

    contact_created.send(None, message=contact_message)

    success = get_config("contact").get("success_message") or (
        "Thanks — we'll be in touch."
    )
    flash(success, "success")
    return redirect(url_for("contact.index"))


# =====================================================================
# ADMIN — inbox
# =====================================================================
@contact_bp.route("/admin/contact", methods=["GET"])
@login_required
def admin_index():
    return render_template(
        "contact/admin/list.html", messages=contact_service.all_messages()
    )


@contact_bp.route("/admin/contact/<int:message_id>/read", methods=["POST"])
@login_required
def admin_read(message_id):
    contact_service.mark_read(message_id)
    flash("Message marked as read.", "success")
    return redirect(url_for("contact.admin_index"))


@contact_bp.route("/admin/contact/<int:message_id>/delete", methods=["POST"])
@login_required
def admin_delete(message_id):
    contact_service.delete_message(message_id)
    flash("Message deleted.", "success")
    return redirect(url_for("contact.admin_index"))
