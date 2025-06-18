# apps/logs/mongo_models.py

from mongoengine import (
    Document, StringField, DateTimeField, FloatField,
    DictField, ListField, IntField, BooleanField
)
import datetime


class LogEntry(Document):
    secret_key = StringField(required=True)
    app_name = StringField(required=True)
    tags = ListField(StringField(), default=[])
    
    endpoint = StringField(required=True)
    method = StringField(required=True)
    status_code = IntField(required=True)
    latency = FloatField(required=True)
    db_execution_time = FloatField()
    response_size = IntField()

    timestamp = DateTimeField(default=datetime.datetime.utcnow)

    request_headers = DictField()
    query_params = DictField()

    user = StringField()
    client_ip = StringField()
    location = StringField(default="Unknown")

    cpu_usage = FloatField()
    memory_usage = FloatField()

    abuse_detected = BooleanField(null=True)
    error = StringField(null=True)

    meta = {
        'collection': 'LogEntry',
        'db_alias': 'mongo',
        'indexes': [
            'secret_key',
            'app_name',
            'endpoint',
            'timestamp',
            '-latency',
            '-status_code',
        ],
        'ordering': ['-timestamp']
    }
