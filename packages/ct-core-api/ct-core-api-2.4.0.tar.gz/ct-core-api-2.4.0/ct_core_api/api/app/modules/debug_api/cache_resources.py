from ct_core_api.api.core import cache, response
from ct_core_api.api.core.namespace import APINamespace
from ct_core_api.api.core.parameters import PostFormParameters
from ct_core_api.api.core.resource import APIResource
from ct_core_api.api.core.response import HTTPStatus
from ct_core_api.api.core.schema import ma

api = APINamespace('cache', description="Caching Utilities")


def _get_cache_region(region):
    try:
        cache_region = cache.dogpile_cache.get_region(region)
    except KeyError:
        cache_region = None
    if not cache_region:
        response.abort(404)
    return cache_region


@api.route('/regions/<string:region>/<string:key>')
class DebugCacheRegionResource(APIResource):
    class PostParameters(PostFormParameters):
        value = ma.Str(required=True, location='form')

    def get(self, region, key):
        """Get value from cache region by key."""
        cache_region = _get_cache_region(region)
        value = cache_region.get(key)
        if value is cache.NO_VALUE:
            response.abort(404)
        return value

    @api.parameters(PostParameters())
    @api.response(code=HTTPStatus.NO_CONTENT)
    def post(self, args, region, key):
        """Set value into cache region at key."""
        cache_region = _get_cache_region(region)
        cache_region.set(key, args['value'])

    @api.response(code=HTTPStatus.NO_CONTENT)
    def delete(self, region, key):
        """Delete value from cache region by key."""
        cache_region = _get_cache_region(region)
        cache_region.delete(key)


@api.route('/regions/<region>/invalidate')
class DebugCacheRegionInvalidateResource(APIResource):

    # FIXME:
    # class PostURLParameters(URLParameters):
    #     region = ma.Str(required=True, validate=validate.OneOf(choices=dogpile_cache_ext.get_cache_region_names()))
    #
    # @api.parameters(PostURLParameters())
    @api.response(code=HTTPStatus.NO_CONTENT)
    def post(self, region):
        """Invalidate cache region."""
        cache_region = _get_cache_region(region)
        cache_region.invalidate()


@api.route('/regions/invalidate-all')
class DebugCacheRegionInvalidateAllResource(APIResource):
    @api.response(code=HTTPStatus.NO_CONTENT)
    def post(self):
        """Invalidate all cache regions."""
        cache.dogpile_cache.invalidate_all_regions()
