
import logging, os, re, time
from glob import glob
from datetime import datetime
import functools
import tornado.web
from bl.dict import Dict, StringDict
from bl.string import String
from bl.url import URL
from bweb.session import Session

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Handler(tornado.web.RequestHandler):

    def initialize(c):
        c.os, c.re, c.time, c.glob, c.datetime = os, re, time, glob, datetime
        c.String = String
        c.config = c.settings.get('config')
        c.url = URL(c.request.full_url(), host=c.settings.host, scheme=c.settings.scheme)
        c.HTTPError = tornado.web.HTTPError
        c.messages = Dict()        

    def arguments(c):
        return StringDict(**c.request.arguments)

    def render(c, template, **kwargs):
        if c not in kwargs:
            kwargs['c'] = c
        super().render(template, **kwargs)

    # def write_error(c, status_code, **kwargs):
    #     c.set_status(status_code)
    #     c.render("http_error.xhtml", status=status_code)

    # == Session management == 

    def init_session(c, new=False, reload=False, expires_days=None, **args):
        """initialize session"""
        if new==True or reload==True or 'session' not in c.__dict__.keys() or c.session is None:
            storage_class_name = c.config.Site.session_storage or 'MemoryStorage'
            if storage_class_name=='FileStorage':
                from bweb.session.file_storage import FileStorage
                c.session_storage = FileStorage(directory=c.config.Site.session_path)
            elif storage_class_name=='DatabaseStorage':
                from bweb.session.database_storage import DatabaseStorage
                c.session_storage = DatabaseStorage(db=c.db)
            elif storage_class_name=='MemcacheStorage':
                from bweb.session.memcache_storage import MemcacheStorage
                c.session_storage = MemcacheStorage(memcache_server=c.config.Site.memcache_server)
            else:
                from bweb.session import MemoryStorage
                c.session_storage = MemoryStorage()
            if new==True: 
                session_id = ''
            else: 
                session_id = (c.get_secure_cookie('session_id') or b'').decode('utf-8')
            c.session = Session.load(c.session_storage, session_id)
            c.set_secure_cookie('session_id', c.session.id.encode('utf-8'), expires_days=expires_days)
        c.session.update(**args)
        
    def reset_session(c):
        """remove the session_id cookie and init a new session."""
        c.clear_cookie('session_id')
        c.init_session(new=True)

    def save_session(c):
        if 'session' in c.__dict__.keys() and c.session is not None:
            c.session.save()

# == decorators == 
def require_login(method):
    """Require the user of this method to be logged in."""
    @functools.wraps(method)
    def wrapper(c, *args, **kwargs):
        if c.session.get('email') is None:
            if c.request.method in ("GET", "HEAD"):
                c.redirect(c.get_login_url()+"?return="+str(c.url))
            else:
                raise tornado.web.HTTPError(403)
        return method(c, *args, **kwargs)
    return wrapper

def require_admin(method):
    """Decorate methods with this to require that the user be logged in with the given role.
    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    If the user is logged in and doesn't have the given role, an HTTP_UNAUTHORIZED error is raised
    """
    @functools.wraps(method)
    def wrapper(c, *args, **kwargs):
        if c.session.get('email') is None:
            if c.request.method in ("GET", "HEAD"):
                url = URL(c.config.Site.url+c.request.path, host=c.request.host, scheme=c.request.protocol)
                # *TODO*: store the 'next' url in the session
                c.redirect(c.get_login_url()+"?ret="+str(url))
                return
            else:
                raise tornado.web.HTTPError(403)
        elif c.session.user.role != 'admin':
            # *TODO*: check to see if the user has the given role
            raise c.HTTPError(401)
        return method(c, *args, **kwargs)
    return wrapper
