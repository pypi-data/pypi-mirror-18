from datetime import timedelta


########################################
# Flask & Extension Configurations
########################################

class _FlaskConfig(object):
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DEBUG = False
    # TESTING
    # PROPAGATE_EXCEPTIONS
    # PRESERVE_CONTEXT_ON_EXCEPTION
    # PERMANENT_SESSION_LIFETIME
    # USE_X_SENDFILE
    # LOGGER_NAME
    # LOGGER_HANDLER_POLICY
    # SERVER_NAME
    # APPLICATION_ROOT
    # SESSION_COOKIE_NAME
    # SESSION_COOKIE_DOMAIN
    # SESSION_COOKIE_PATH
    # SESSION_COOKIE_HTTPONLY
    # SESSION_COOKIE_SECURE
    # SESSION_REFRESH_EACH_REQUEST
    # MAX_CONTENT_LENGTH
    # SEND_FILE_MAX_AGE_DEFAULT
    # TRAP_BAD_REQUEST_ERRORS
    # TRAP_HTTP_EXCEPTIONS
    # EXPLAIN_TEMPLATE_LOADING
    # PREFERRED_URL_SCHEME
    # JSON_AS_ASCII
    # JSON_SORT_KEYS
    # JSONIFY_PRETTYPRINT_REGULAR
    # JSONIFY_MIMETYPE
    # TEMPLATES_AUTO_RELOAD


class _APIConfig(object):
    # Path to the API changelog entries in YAML format
    API_CHANGELOG_PATH = None  # Defaults to `<current_app.root_path>/changelog.yml`

    # The warning message for deprecated API endpoints will be logged
    # if the `deprecated_on` datetime is within this window
    API_DEPRECATED_ENDPOINT_WARNING_WINDOW = timedelta(weeks=1)

    API_CACHE_ENABLED = True
    API_CACHE_DEBUG_LOGGING = True

    API_TEST_CACHE_REGION = 'api.test'
    API_RESOURCE_RESPONSE_DATA__SHORT_CACHE_REGION = 'api.resource.response.data--short'
    API_RESOURCE_RESPONSE_DATA__MEDIUM_CACHE_REGION = 'api.resource.response.data--medium'
    API_RESOURCE_RESPONSE_DATA__LONG_CACHE_REGION = 'api.resource.response.data--long'


class _RestPlusConfig(object):
    RESTPLUS_VALIDATE = False
    RESTPLUS_MASK_HEADER = 'X-Fields'
    RESTPLUS_MASK_SWAGGER = False
    ERROR_404_HELP = False


class _SQLAlchemyConfig(object):
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False


class _SQLAlchemyLoggingConfig(object):
    # Enable connection pool logging
    POOL_DEBUG_LOGGING = False

    # SQLAlchemy event debug logging (prints event debug information to std out)
    SQLA_EVENT_DEBUG_LOGGING = False
    SQLA_EXECUTE_EVENT_DEBUG_LOGGING = False  # Include "execute" events in the event debug logging


class _SwaggerUIConfig(object):
    SWAGGER_UI_JSONEDITOR = True
    # SWAGGER_UI_OAUTH_CLIENT_ID = 'swagger-ui-oauth2-client'
    # SWAGGER_UI_OAUTH_REALM = "swagger-ui-oauth2-realm"
    # SWAGGER_UI_OAUTH_APP_NAME = "swagger-ui-oauth2-app-name"


class _RemoteDebuggingConfig(object):
    REMOTE_DEBUG = False
    REMOTE_DEBUG_IP = '192.168.7.1'
    REMOTE_DEBUG_PORT = 34153


class _CORSConfig(object):
    CSRF_ENABLED = True


class _DogpileCacheConfig(object):
    DOGPILE_CACHE_URLS = ['0.0.0.0:11211']  # Overridden by per-environment settings
    DOGPILE_CACHE_BACKEND = 'dogpile.cache.memcached'
    DOGPILE_CACHE_DEFAULT_EXPIRATION = 60  # Seconds
    DOGPILE_CACHE_ARGUMENTS = {'distributed_lock': True}

    DOGPILE_CACHE_REGIONS = [
        (_APIConfig.API_TEST_CACHE_REGION, DOGPILE_CACHE_DEFAULT_EXPIRATION),
        (_APIConfig.API_RESOURCE_RESPONSE_DATA__SHORT_CACHE_REGION, 60),  # 1 minute
        (_APIConfig.API_RESOURCE_RESPONSE_DATA__MEDIUM_CACHE_REGION, 10 * 60),  # 10 minutes
        (_APIConfig.API_RESOURCE_RESPONSE_DATA__LONG_CACHE_REGION, 60 * 60)]  # 1 hour


class _CeleryConfig(object):
    # 'amqp://{{ rabbitmq_user }}:{{ rabbitmq_password }}@{{ rabbitmq_host }}:5672/{{ rabbitmq_vhost }}'
    CELERY_BROKER_URL = None
    # 'db+mysql://{{ db_web_user }}:{{ db_web_password }}@{{ db_host }}:3306/{{ db_application_name }}'
    CELERY_RESULT_BACKEND = None

    CELERY_BEAT_NUM_PROCESSES = 1
    CELERY_WORKER_NUM_PROCESSES = 1

    CELERY_SEND_TASK_ERROR_EMAILS = False
    CELERY_TIMEZONE = 'UTC'
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    CELERYBEAT_SCHEDULE = {}


class _AppExtensionsConfig(
        _APIConfig,
        _RestPlusConfig,
        _SQLAlchemyConfig,
        _SQLAlchemyLoggingConfig,
        _SwaggerUIConfig,
        _DogpileCacheConfig,
        _CORSConfig,
        _CeleryConfig,
        _RemoteDebuggingConfig):
    pass


########################################
# App "Mode" Configurations
########################################

class BaseConfig(_FlaskConfig, _AppExtensionsConfig):
    AVAILABLE_MODULES = ['index', 'health', 'debug_api', 'swagger_ui']
    AVAILABLE_EXTENSIONS = [
        'debug_api_ext',
        'celery_ext',
        'cors_ext',
        'dogpile_cache_ext',
        'login_manager_ext',
        'marshmallow_ext',
        'sqlalchemy_ext',
        'uuid_ext',
        'oauth2_ext']

    ENABLED_MODULES = AVAILABLE_MODULES
    ENABLED_EXTENSIONS = filter(lambda x: x not in {'oauth2_ext', 'uuid_ext'}, AVAILABLE_EXTENSIONS)

    # The current git revision hash
    GIT_REVISION = None

    # Format JSON within the API response payloads by sorting keys and indenting with 4 spaces
    INDENT_AND_SORT_JSON = True

    # Log level for our application
    # Overriding this will set the log level for the app logger
    LOG_LEVEL = None

    # Log message format: log record creation time, log level, source file path, source line number, message
    LOG_MSG_FORMAT = "\n[%(asctime)s][%(levelname)s][%(pathname)s:%(lineno)d]\n%(message)s"

    # Log message date format (affects date formatting params like `asctime`)
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S %Z%z"

    # Logs extra contextual request information as part of the exception message itself
    LOG_EXTRA_REQUEST_INFO_ON_REQUEST_EXCEPTION = False

    # When in debug mode, send exception message and stack trace to the browser's console via the response headers
    LOG_EXCEPTIONS_TO_BROWSER_CONSOLE = False

    # When in debug mode, log verbose development messages
    LOG_VERBOSE_DEV_MESSAGES = False

    # When in debug mode, log a summary of the SQL queries gathered by Flask-SQLAlchemy during the course of a request
    LOG_DEBUG_SQL_QUERIES = False


class ProductionConfig(BaseConfig):
    # Exclude the debug extension and modules
    ENABLED_MODULES = filter(lambda x: x not in {'debug', 'debug_api'}, BaseConfig.ENABLED_MODULES)
    ENABLED_EXTENSIONS = filter(lambda x: x not in {'debug_api_ext'}, BaseConfig.ENABLED_EXTENSIONS)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOG_VERBOSE_DEV_MESSAGES = True


class TestingConfig(BaseConfig):
    TESTING = True
    LOG_LEVEL = 'WARNING'

    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # Use in-memory SQLite database for testing

    API_CACHE_ENABLED = False
