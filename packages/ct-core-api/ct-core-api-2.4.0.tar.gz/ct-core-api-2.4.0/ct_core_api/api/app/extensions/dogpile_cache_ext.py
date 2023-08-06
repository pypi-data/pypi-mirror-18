from dogpile.cache.api import NO_VALUE
from dogpile.cache.proxy import ProxyBackend
from flask import current_app, has_request_context

from ct_core_api.api.app import config
from ct_core_api.api.core import cache


########################################
# Dogpile-Cache Extension
########################################

def init_app(app):
    wrappers_debug = [SettingsAwareProxyCacheBackend]
    wrappers_production = [SettingsAwareProxyCacheBackend]

    # If debug logging is enabled then the caching operations will log debug messages through this proxy
    if is_cache_debug_logging_enabled(app):
        wrappers_debug.append(DebugLoggingProxyCacheBackend)

    cache.dogpile_cache.init_app(app, wrappers_debug=wrappers_debug, wrappers_production=wrappers_production)


########################################
# Dogpile-Cache Helpers
########################################

def is_cache_enabled(app=None):
    app = app or current_app
    return app.config.get('API_CACHE_ENABLED', True)


def is_cache_debug_logging_enabled(app=None):
    app = app or current_app
    return app.config.get('API_CACHE_DEBUG_LOGGING', True)


def enable_cache(app=None):
    app = app or current_app
    app.config['API_CACHE_ENABLED'] = True


def disable_cache(app=None):
    app = app or current_app
    app.config['API_CACHE_ENABLED'] = False


def get_cache_urls(app=None):
    app = app or current_app
    return app.config.get('DOGPILE_CACHE_URLS', [])


def get_cache_region_names():
    if has_request_context():
        cache_regions = cache.dogpile_cache.get_all_regions()
        return cache_regions.keys()
    else:
        cache_regions = dict(config.BaseConfig.DOGPILE_CACHE_REGIONS)
        return cache_regions.keys()


def get_cache_region_expiration_time(region):
    if isinstance(region, (str, unicode)):
        if has_request_context():
            cache_region = cache.dogpile_cache.get_region(region)
            return cache_region.expiration_time
        else:
            cache_regions = dict(config.BaseConfig.DOGPILE_CACHE_REGIONS)
            return cache_regions.get(region)
    else:
        return region.expiration_time


########################################
# Cache Proxy Backends
########################################

class DebugLoggingProxyCacheBackend(ProxyBackend):
    """A cache proxy that logs debug messages for every cache operation."""

    def get(self, key):
        value = self.proxied.get(key)
        current_app.logger.debug("$$$ cache.get({!r}) = {!r}".format(key, value))
        return value

    def set(self, key, value):
        current_app.logger.debug("$$$ cache.set({!r}, {!r})".format(key, value))
        self.proxied.set(key, value)

    def delete(self, key):
        current_app.logger.debug("$$$ cache.delete({!r})".format(key))
        self.proxied.delete(key)

    def get_multi(self, keys):
        values = self.proxied.get_multi(keys)
        current_app.logger.debug("$$$ cache.get_multi({!r}) = {!r}".format(keys, values))

    def set_multi(self, keys):
        current_app.logger.debug("$$$ cache.set_multi({!r}, {!r})".format(keys.keys(), keys.values()))
        self.proxied.set_multi(keys)

    def delete_multi(self, keys):
        current_app.logger.debug("$$$ cache.delete_multi({!r})".format(keys))
        self.proxied.delete_multi(keys)

    def get_mutex(self, key):
        # current_app.logger.debug("$$$ cache.get_mutex({!r})".format(key))
        return self.proxied.get_mutex(key)


class SettingsAwareProxyCacheBackend(ProxyBackend):
    """A cache proxy that uses application settings to determine whether a cache operation should execute."""

    def get(self, key):
        if is_cache_enabled():
            return self.proxied.get(key)
        return NO_VALUE

    def set(self, key, value):
        if is_cache_enabled():
            self.proxied.set(key, value)

    def delete(self, key):
        if is_cache_enabled():
            self.proxied.delete(key)

    def get_multi(self, keys):
        if is_cache_enabled():
            return self.proxied.get_multi(keys)
        return NO_VALUE

    def set_multi(self, keys):
        if is_cache_enabled():
            self.proxied.set_multi(keys)

    def delete_multi(self, keys):
        if is_cache_enabled():
            self.proxied.delete_multi(keys)

    def get_mutex(self, key):
        if is_cache_enabled():
            return self.proxied.get_mutex(key)
