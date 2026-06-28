from splent_io.splent_feature_contact.models import ContactMessage
from splent_framework.repositories.BaseRepository import BaseRepository


class ContactRepository(BaseRepository):
    def __init__(self):
        super().__init__(ContactMessage)

    def all_newest_first(self) -> list[ContactMessage]:
        return ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()

    def pending(self) -> list[ContactMessage]:
        return (
            ContactMessage.query.filter_by(read=False)
            .order_by(ContactMessage.created_at.desc())
            .all()
        )
