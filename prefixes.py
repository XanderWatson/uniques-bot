import mongoengine
import datetime


class Prefix(mongoengine.Document):
    _guild_name = mongoengine.StringField()
    _guild_id = mongoengine.StringField(unique=True)
    _guild_join_date = mongoengine.DateTimeField(
        default=datetime.datetime.now())
    _prefix = mongoengine.StringField()
