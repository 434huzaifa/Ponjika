
from flask_login import UserMixin
from datetime import datetime
from mongoengine import EmbeddedDocument,Document,StringField,EmailField,DateTimeField,URLField,ReferenceField,EmbeddedDocumentListField,CASCADE,ListField,ObjectIdField
from bson.objectid import ObjectId

class User(Document,UserMixin):
    name=StringField()
    username=StringField(unique=True)
    email=EmailField(unique=True)
    password=StringField()
    image=StringField(default='broken_image.jpg')
    datetime=DateTimeField(default=datetime.now())

class Items(EmbeddedDocument):
    id=ObjectIdField(default=ObjectId,unique=True,required=True,primary_key=True)
    title=StringField(required=True)
    link=URLField(null=True)
    about=StringField(null=True)
    item_type=StringField(null=True)
    
    image=StringField(default='broken_image.jpg')

class Lists(Document):
    title=StringField(requird=True)
    about=StringField(null=True)
    user=ReferenceField('User',reverse_delete_rule=CASCADE,requird=True,unique_with='title')
    image=StringField(default='broken_image.jpg')
    items=EmbeddedDocumentListField(Items,default=[])
    datetime=DateTimeField(default=datetime.now())




def lists_is_exist(title):
    lists=Lists.objects(title=title)
    if lists:
        return False
    return True