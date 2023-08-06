# -*- coding: utf-8 -*-
from aiohttp import web
from pkg_resources import iter_entry_points
from plone.server import app_settings
from plone.server.async import IAsyncUtility
from plone.server.auth.validators import hash_password
from plone.server.auth.users import ROOT_USER_ID
from plone.server.auth.users import RootUser
from plone.server.content import IStaticDirectory
from plone.server.content import IStaticFile
from plone.server.content import StaticFile
from plone.server.contentnegotiation import ContentNegotiatorUtility
from plone.server.interfaces import IApplication
from plone.server.interfaces import IContentNegotiation
from plone.server.interfaces import IDataBase
from plone.server.transactions import RequestAwareDB
from plone.server.transactions import RequestAwareTransactionManager
from plone.server.traversal import TraversalRouter
from plone.server.utils import import_class
from plone.server.content import loadCachedSchema
from ZEO.ClientStorage import ClientStorage
from ZODB import DB
from ZODB.DemoStorage import DemoStorage
from zope.component import getAllUtilitiesRegisteredFor
from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.component import provideUtility
from zope.configuration.config import ConfigurationConflictError
from zope.configuration.config import ConfigurationMachine
from zope.configuration.xmlconfig import include
from zope.configuration.xmlconfig import registerCommonDirectives
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.securitypolicy.principalpermission import PrincipalPermissionManager

import asyncio
import json
import logging
import sys
import transaction
import ZODB.FileStorage


try:
    from Crypto.PublicKey import RSA
except ImportError:
    RSA = None

logger = logging.getLogger(__name__)


@implementer(IApplication)
class ApplicationRoot(object):

    root_user = None

    def __init__(self, config_file):
        self._dbs = {}
        self._config_file = config_file
        self._async_utilities = {}

    def add_async_utility(self, config):
        interface = import_class(config['provides'])
        factory = import_class(config['factory'])
        utility_object = factory(config['settings'])
        provideUtility(utility_object, interface)
        task = asyncio.ensure_future(utility_object.initialize(app=self))
        self.add_async_task(config['provides'], task, config)

    def add_async_task(self, ident, task, config):
        if ident in self._async_utilities:
            raise KeyError("Already exist an async utility with this id")
        self._async_utilities[ident] = {
            'task': task,
            'config': config
        }

    def cancel_async_utility(self, ident):
        if ident in self._async_utilities:
            self._async_utilities[ident]['task'].cancel()
        else:
            raise KeyError("Ident does not exist as utility")

    def del_async_utility(self, config):
        self.cancel_async_utility(config['provides'])
        interface = import_class(config['provides'])
        utility = getUtility(interface)
        gsm = getGlobalSiteManager()
        gsm.unregisterUtility(utility, provided=interface)

    def set_root_user(self, user):
        password = user['password']
        if password:
            password = hash_password(password)
        self.root_user = RootUser(password)

    def __contains__(self, key):
        return True if key in self._dbs else False

    def __len__(self):
        return len(self._dbs)

    def __getitem__(self, key):
        return self._dbs[key]

    def __delitem__(self, key):
        """ This operation can only be done throw HTTP request

        We can check if there is permission to delete a site
        XXX TODO
        """

        del self._dbs[key]

    def __iter__(self):
        return iter(self._dbs.items())

    def __setitem__(self, key, value):
        """ This operation can only be done throw HTTP request

        We can check if there is permission to delete a site
        XXX TODO
        """

        self._dbs[key] = value


class DataBaseToJson(object):

    def __init__(self, dbo, request):
        self.dbo = dbo

    def __call__(self):
        return {
            'sites': self.dbo.keys()
        }


class ApplicationToJson(object):

    def __init__(self, application, request):
        self.application = application
        self.request = request

    def __call__(self):
        result = {
            'databases': [],
            'static_file': [],
            'static_directory': []
        }

        allowed = self.request.security.checkPermission(
            'plone.GetDatabases', self.application)

        for x in self.application._dbs.keys():
            if IDataBase.providedBy(self.application._dbs[x]) and allowed:
                result['databases'].append(x)
            if IStaticFile.providedBy(self.application._dbs[x]):
                result['static_file'].append(x)
            if IStaticDirectory.providedBy(self.application._dbs[x]):
                result['static_directory'].append(x)
        return result


class RootSpecialPermissions(PrincipalPermissionManager):
    """No Role Map on Application and DB so permissions set to users.

    It will not affect Plone sites as they don't have parent pointers to DB/APP
    """
    def __init__(self, db):
        super(RootSpecialPermissions, self).__init__()
        self.grantPermissionToPrincipal('plone.AddPortal', ROOT_USER_ID)
        self.grantPermissionToPrincipal('plone.GetPortals', ROOT_USER_ID)
        self.grantPermissionToPrincipal('plone.DeletePortals', ROOT_USER_ID)
        self.grantPermissionToPrincipal('plone.AccessContent', ROOT_USER_ID)
        self.grantPermissionToPrincipal('plone.GetDatabases', ROOT_USER_ID)
        self.grantPermissionToPrincipal('plone.GetAPIDefinition', ROOT_USER_ID)
        # Access anonymous - needs to be configurable
        self.grantPermissionToPrincipal(
            'plone.AccessContent', 'Anonymous User')


@implementer(IDataBase)
class DataBase(object):
    def __init__(self, id, db):
        self.id = id
        self._db = db
        self._conn = None
        self.tm_ = RequestAwareTransactionManager()

    def open(self):
        tm_ = RequestAwareTransactionManager()
        return self._db.open(transaction_manager=tm_)

    def _open(self):
        self._conn = self._db.open(transaction_manager=self.tm_)

        @self._conn.onCloseCallback
        def on_close():
            self._conn = None

    @property
    def conn(self):
        if self._conn is None:
            self._open()
        return self._conn

    @property
    def _p_jar(self):
        if self._conn is None:
            self._open()
        return self._conn

    def __getitem__(self, key):
        # is there any request active ? -> conn there
        return self.conn.root()[key]

    def keys(self):
        return list(self.conn.root().keys())

    def __setitem__(self, key, value):
        """ This operation can only be done throw HTTP request

        We can check if there is permission to delete a site
        XXX TODO
        """
        self.conn.root()[key] = value

    def __delitem__(self, key):
        """ This operation can only be done throw HTTP request

        We can check if there is permission to delete a site
        XXX TODO
        """

        del self.conn.root()[key]

    def __iter__(self):
        return iter(self.conn.root().items())

    def __contains__(self, key):
        # is there any request active ? -> conn there
        return key in self.conn.root()

    def __len__(self):
        return len(self.conn.root())


async def close_utilities(app):
    for utility in getAllUtilitiesRegisteredFor(IAsyncUtility):
        asyncio.ensure_future(utility.finalize(app=app), loop=app.loop)


def make_app(config_file=None, settings=None):

    # Initialize aiohttp app
    app = web.Application(router=TraversalRouter())

    if config_file is not None:
        with open(config_file, 'r') as config:
            settings = json.load(config)
    elif settings is not None:
        settings = settings
    else:
        raise Exception('Neither configuration or settings')

    # with settings, update app_settings, where defaults are defined and
    # we setup the app from
    for key, value in settings.items():
        if isinstance(app_settings.get(key), dict):
            app_settings[key].update(value)
        else:
            app_settings[key] = value

    # Create root Application
    root = ApplicationRoot(config_file)
    root.app = app
    provideUtility(root, IApplication, 'root')

    # Initialize global (threadlocal) ZCA configuration
    app.config = ConfigurationMachine()
    registerCommonDirectives(app.config)

    include(app.config, 'configure.zcml', sys.modules['plone.server'])
    for ep in iter_entry_points('plone.server'):  # auto-include applications
        include(app.config, 'configure.zcml', ep.load())
    try:
        app.config.execute_actions()
    except ConfigurationConflictError as e:
        logger.error(str(e._conflicts))
        raise e

    content_type = ContentNegotiatorUtility(
        'content_type', app_settings['renderers'].keys())
    language = ContentNegotiatorUtility(
        'language', app_settings['languages'].keys())

    provideUtility(content_type, IContentNegotiation, 'content_type')
    provideUtility(language, IContentNegotiation, 'language')

    for database in app_settings['databases']:
        for key, dbconfig in database.items():
            config = dbconfig.get('configuration', {})
            if dbconfig['storage'] == 'ZODB':
                # Open it not Request Aware so it creates the root object
                fs = ZODB.FileStorage.FileStorage(dbconfig['path'])

                db = DB(fs)
                try:
                    if not IDataBase.providedBy(root):
                        alsoProvides(db.open().root(), IDataBase)
                    transaction.commit()
                except:
                    pass
                finally:
                    db.close()
                # Set request aware database for app
                db = RequestAwareDB(dbconfig['path'], **config)
                dbo = DataBase(key, db)
            elif dbconfig['storage'] == 'ZEO':
                # Try to open it normal to create the root object
                address = (dbconfig['address'], dbconfig['port'])

                cs = ClientStorage(address)
                db = DB(cs)

                try:
                    if not IDataBase.providedBy(root):
                        alsoProvides(db.open().root(), IDataBase)
                    transaction.commit()
                except:
                    pass
                finally:
                    db.close()

                # Set request aware database for app
                cs = ClientStorage(address)
                db = RequestAwareDB(cs, **config)
                dbo = DataBase(key, db)
            elif dbconfig['storage'] == 'DEMO':
                storage = DemoStorage(name=dbconfig['name'])
                db = DB(storage)
                alsoProvides(db.open().root(), IDataBase)
                transaction.commit()
                db.close()
                # Set request aware database for app
                db = RequestAwareDB(storage)
                dbo = DataBase(key, db)
            root[key] = dbo

    for static in app_settings['static']:
        for key, file_path in static.items():
            root[key] = StaticFile(file_path)

    root.set_root_user(app_settings['root_user'])

    if RSA is not None and not app_settings.get('rsa'):
        key = RSA.generate(2048)
        pub_jwk = {'k': key.publickey().exportKey('PEM')}
        priv_jwk = {'k': key.exportKey('PEM')}
        app_settings['rsa'] = {
            'pub': pub_jwk,
            'priv': priv_jwk
        }

    # Set router root
    app.router.set_root(root)

    for utility in getAllUtilitiesRegisteredFor(IAsyncUtility):
        # In case there is Utilties that are registered from zcml
        ident = asyncio.ensure_future(utility.initialize(app=app), loop=app.loop)
        root.add_async_utility(ident, {})

    app.on_cleanup.append(close_utilities)

    for util in app_settings['utilities']:
        root.add_async_utility(util)

    # Load cached Schemas
    loadCachedSchema()

    return app
