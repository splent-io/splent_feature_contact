from datetime import datetime

from splent_framework.db import db


class ContactMessage(db.Model):
    """A message submitted through the public contact form.

    Stored even when the notification email fails to send, so nothing is lost.
    ``read`` flags whether an admin has triaged it.
    """

    __tablename__ = "contact_message"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), default="")
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False, index=True)

    def __repr__(self):
        return f"ContactMessage<{self.id} from {self.email}>"
