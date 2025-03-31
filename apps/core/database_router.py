class DatabaseRouter:
    """
    A router to control database operations on models based on their app_label.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'analytics':
            return 'mongo'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'analytics':
            return 'mongo'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'analytics':
            return db == 'mongo'
        return db == 'default'
