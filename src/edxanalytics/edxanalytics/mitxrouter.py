## This is a dummy router for now
##
## In the future, it will route read replica calls to the right place
import logging

log=logging.getLogger(__name__)

class MITxRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['student','courseware', 'contenttypes']:
            return 'remote'
        elif model._meta.app_label in ['an_evt','edxmodules', 'djmodules', 'cronjobs', 'celery', 'sessions', 'auth', 'django_cache', 'south', 'sites']:
            return 'default'
        else:
            log.error("We need to explicitly route: {0}".format(model._meta.app_label))
            return 'error'

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        #if model._meta.app_label == 'auth':
        #    return 'auth_db'
        print "db_for_write", model
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        #if obj1._meta.app_label == 'auth' or \
        #   obj2._meta.app_label == 'auth':
        #   return True
        print "allow_relation", obj1, obj2

        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        print "allow_syncdb", db, model
        #if db == 'auth_db':
        #    return model._meta.app_label == 'auth'
        #elif model._meta.app_label == 'auth':
        #    return False
        return None
