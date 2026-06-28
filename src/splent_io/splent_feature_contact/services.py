from splent_io.splent_feature_contact.models import ContactMessage
from splent_io.splent_feature_contact.repositories import ContactRepository
from splent_framework.services.BaseService import BaseService


class ContactService(BaseService):
    def __init__(self):
        super().__init__(ContactRepository())

    def all_messages(self):
        """Every message, newest first."""
        return self.repository.all_newest_first()

    def pending_count(self) -> int:
        """How many messages are still unread (for the sidebar badge)."""
        return ContactMessage.query.filter_by(read=False).count()

    def create_message(self, name, email, subject, message):
        """Persist a submitted contact message and return it."""
        return self.repository.create(
            name=name,
            email=email,
            subject=subject or "",
            message=message,
            read=False,
        )

    def mark_read(self, message_id):
        """Flag a message as read."""
        return self.repository.update(message_id, read=True)

    def delete_message(self, message_id):
        """Remove a message permanently."""
        return self.repository.delete(message_id)
