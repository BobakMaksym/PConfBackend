from mongoengine import Document, StringField


class BaseComponentDocument(Document):
    meta = {"abstract": True, "db_alias": "default"}

    manufacturer: str = StringField(required=True)
    model: str = StringField(required=True)
