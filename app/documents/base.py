from mongoengine import Document, StringField


class BaseDocument(Document):
    meta = {"abstract": True, "db_alias": "default"}

    manufacturer = StringField(required=True)
    model = StringField(required=True)
