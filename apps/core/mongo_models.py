from mongoengine import Document, StringField, IntField, FloatField, DateTimeField, DictField
import datetime

class Endpoint(Document):
    access_key = StringField(required=True)  
    app_name = StringField()
    path = StringField(required=True)       
    method = StringField(required=True)     
    
    last_status_code = IntField()
    average_latency = FloatField(default=0)
    average_db_time = FloatField(default=0)
    total_requests = IntField(default=0)
    total_failures = IntField(default=0)

    tags = DictField() 
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'db_alias': 'mongo',
        'indexes': [
            {'fields': ['access_key', 'path', 'method'], 'unique': True}
        ]
    }
