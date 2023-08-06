from .base import *
from datetime import timedelta
from urllib.parse import urlparse

##########
# Django #
##########
INSTALLED_APPS += [
    # 'raven.contrib.django.raven_compat',
    # 'munch_storage',
    # Other
    # 'debug_toolbar',
    'munch_dentifrice'
]
# MIDDLEWARE_CLASSES.insert(MIDDLEWARE_CLASSES.index('django.middleware.common.CommonMiddleware') - 1, 'corsheaders.middleware.CorsMiddleware')  # noqa
# CORS_ORIGIN_ALLOW_ALL = True
DEBUG = True
SECRET_KEY = 'test'
CONTAINER_IP = urlparse(os.environ.get(
    'DOCKER_HOST', 'tcp://localhost')).hostname
BROKER_URL = 'amqp://guest:guest@{}:5682/munch'.format(CONTAINER_IP)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'munch',
        'USER': 'munch',
        'PASSWORD': 'munch',
        'HOST': CONTAINER_IP,
        'PORT': '15432',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:16379/1".format(CONTAINER_IP),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# MIDDLEWARE_CLASSES += ['munch.settings.local.NonHtmlDebugToolbarMiddleware']


class NonHtmlDebugToolbarMiddleware:
    """
    The Django Debug Toolbar usually only works for views that return HTML.
    This middleware wraps any non-HTML response in HTML if the request
    has a 'debug' query parameter (e.g. http://localhost/foo?debug)
    Special handling for json (pretty printing) and
    binary data (only show data length)
    """

    @staticmethod
    def process_response(request, response):
        import json
        from django.http import HttpResponse

        if request.GET.get('debug') == '':
            if response['Content-Type'] == 'application/octet-stream':
                new_content = '<html><body>Binary Data, ' \
                    'Length: {}</body></html>'.format(len(response.content))
                response = HttpResponse(new_content)
            elif response['Content-Type'] != 'text/html':
                content = response.content
                try:
                    json_ = json.loads(content.decode('utf-8'))
                    content = json.dumps(json_, sort_keys=True, indent=2)
                except ValueError:
                    pass
                response = HttpResponse('<html><body><pre>{}'
                                        '</pre></body></html>'.format(content))

        return response

###########
# Logging #
###########
"""
RAVEN_CONFIG = {
    'dsn': 'http://13a320fda9ef4ae39c7a9b7f724859ef:6547c908892548a3863c379398f24090@localhost:9000/2',
}
"""
LOGGING['loggers']['munch'] = {
    'handlers': ['console'],
    'filters': [],
    'propagate': False,
    'level': logging.DEBUG,
}
LOGGING['loggers']['munch_mailsend'] = {
    'handlers': ['console'],
    'level': logging.DEBUG,
    'propagate': False
}
"""
LOGGING['disable_existing_loggers'] = True
LOGGING['handlers']['sentry'] = {
    'level': 'ERROR',
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}
LOGGING['loggers']['root'] = {
    'handlers': ['console', 'sentry'],
    'level': 'WARNING',
}
LOGGING['loggers']['raven'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
    'propagate': False,
}
LOGGING['loggers']['sentry.errors'] = {
    'level': 'DEBUG',
    'handlers': ['console'],
    'propagate': False,
}
"""

##########
# Global #
##########
APPLICATION_URL = 'http://localhost:8000'
MASS_SENDER_DOMAIN = 'localhost'
BYPASS_DNS_CHECKS = True
MASS_EMAIL_BACKEND = 'munch_mailsend.backend.Backend'

##################
# Custom headers #
##################
X_POOL_HEADER = 'X-CM-Pool'

##########
# Celery #
##########
CELERYBEAT_SCHEDULE.update({
    'ping_workers': {
        'task': 'mailsend.tasks.ping_workers',
        'schedule': timedelta(seconds=30),
    },
    'check_disabled_workers': {
        'task': 'mailsend.tasks.check_disabled_workers',
        'schedule': timedelta(seconds=30),
    }
})

#################
# Transactional #
#################
TRANSACTIONAL['PROXYPROTO_ENABLED'] = False
TRANSACTIONAL['SMTP_BIND_HOST'] = '0.0.0.0'
TRANSACTIONAL['SMTP_BIND_PORT'] = 1035
TRANSACTIONAL['SMTP_SMARTHOST_TLS'] = {
    'keyfile': os.path.join(
        BASE_DIR, '../../utils/ssl/postfix.example.com.key.pem'),
    'certfile': os.path.join(
        BASE_DIR, '../../utils/ssl/postfix.example.com.cert.pem'),
}
TRANSACTIONAL['HEADERS_TO_REMOVE'] += [X_POOL_HEADER]


############
# Mailsend #
############
MAILSEND = {
    # All Internal mailsend emails will be send to a blackhole
    'SANDBOX': False,
    'SMTP_WORKER_FORCE_MX': [{
        'domain': 'example.com',
        'destination': CONTAINER_IP, 'port': '2525'
    }],
    'RELAY_TIMEOUTS': {
        'connect_timeout': 30.0, 'command_timeout': 30.0,
        'data_timeout': None, 'idle_timeout': None},
    # Timeout for MailStatus cache
    'MAILSTATUS_CACHE_TIMEOUT': 60 * 60 * 24 * 15,
    'X_USER_ID_HEADER': X_USER_ID_HEADER,
    'X_POOL_HEADER': X_POOL_HEADER,
    'X_MESSAGE_ID_HEADER': X_MESSAGE_ID_HEADER,
    # Letting to None will make it use the host FQDN
    'SMTP_WORKER_EHLO_AS': 'localhost',
    # Letting to None fallback to system routing
    # example: '1.2.3.4'
    'SMTP_WORKER_SRC_ADDR': '127.0.0.1',
    # Backoff time is exponentially growing up to max_retry_interval and then
    # staying there on each retry till we reach time_before_drop.
    'RETRY_POLICY': {
        # Minimun time between two retries
        'min_retry_interval': 600,
        # Maximum time between two retries
        'max_retry_interval': 3600,
        # Time before we drop the mail and notify sender
        'time_before_drop': 2 * 24 * 3600},
    'BINARY_ENCODER': None,
    'BLACKLISTED_HEADERS': [
        X_POOL_HEADER,
        X_HTTP_DSN_RETURN_PATH_HEADER,
        X_SMTP_DSN_RETURN_PATH_HEADER],
    'RELAY_POLICIES': [
        'munch.apps.transactional.policies.relay.headers.RewriteReturnPath',
        'mailsend.policies.relay.headers.StripBlacklisted',
        'mailsend.policies.relay.dkim.Sign'],
    'WORKER_POLICIES': [
        'mailsend.policies.mx.pool.Policy',
        'mailsend.policies.mx.rate_limit.Policy',
        'mailsend.policies.mx.greylist.Policy',
        'mailsend.policies.mx.warm_up.Policy'],
    'WORKER_POLICIES_SETTINGS': {
        'rate_limit': {
            'domains': [
                (r'.*', 2)],
            'max_queued': 60 * 15},
        'warm_up': {
            'prioritize': 'equal',
            'domain_warm_up': {
                'matrix': [50, 100, 300, 500, 1000],
                'goal': 500,
                'max_tolerance': 10,
                'step_tolerance': 10,
                'days_watched': 10,
            },
            'ip_warm_up': {
                'matrix': [50, 100, 300, 500, 1000],
                'goal': 500,
                'max_tolerance': 10,
                'step_tolerance': 10,
                'enabled': False,
                'days_watched': 10,
            }
        },
        'pool': {'pools': ['default']},
        'greylist': {'min_retry': 60 * 5},
    },
    'WARM_UP_DOMAINS': {},
    'DKIM_PRIVATE_KEY': """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDiTemlcIMSRZ3us+cSt8Z9SjJ3H49FPq2BoT6IIbYX0PGj3jhu
HsyqX+NLpjCgtKAWMw4ik3sjTkTz56NRxOavvzif4gTSg4/d6VmHs5Mw4/HSjMrZ
9+vDhC3Wt5heQSOvyIwKj8+KgyGRRRmoZbmDN4ms0Gq1OFIHm4T7mQP28wIDAQAB
AoGAEbpkyU8NFYtame6B9Zdr9ziux2IziQsl8He/PE7XwvndVCb+aLIE+nvUhIKa
YJyFxfdt7gt7pAJnqGvHAYrZP1mKsZDIkEgFruYwNVGCLkIQDk3RJwNb3Qpgwskj
mJnQVLZOE120NxBXqrIvNz0Gi61H08gUB5TFKUM3bFxc38ECQQD9X+kmwElyc+Oa
EYJIO6NuvVoDJQBZX+tuaUuomAbqejoMgo5njdFKLR+IqBO43lG9FAitgWCanyvh
S/eoGqKRAkEA5KYyUdl5lHOxHcLo6VKT7Y9nZBPoWn0QhMYuN6vJDpzEr9S+4sSH
CCbawaJGxrJFIiA4vBodOjvIQwOur1Q7QwJBAOHzwiv4locmqfYfXxujc5+x5K+h
M6qAS6fu5rW2vZQk49d8Jhpa8iVAEDsCCHR4blQ7pXF1Sv0YrT0BTh3vgsECQB/q
gwOh07LBI2wAFPrcqAF1Dv2NOdXHt1KRR0pGFF6Ry3Kvw6VrwV2F7uswd6isobHN
xZ2cF5BVX/LaxLt8inkCQQCFKnTfKaEp4W90zqBUWZn+M6zRZfyi+2gN95Srikra
DxEoQHGETi2ZDSihkvx/spwT3r8kNvfTYXpgwt14l0jq
-----END RSA PRIVATE KEY-----""",
    'DKIM_SELECTOR': "test",
    'TLS': {
        'keyfile': os.path.join(
            BASE_DIR, '../../utils/ssl/postfix.example.com.key.pem'),
        'certfile': os.path.join(
            BASE_DIR, '../../utils/ssl/postfix.example.com.cert.pem')},
}

#############
# Campaigns #
#############
CAMPAIGNS['SKIP_SPAM_CHECK'] = True
CAMPAIGNS['SKIP_VIRUS_CHECK'] = True
CAMPAIGNS['BYPASS_RECIPIENTS_MX_CHECK'] = True

############
# Contacts #
############
CONTACTS = {
    # How many contacts can we add in a single API request ?
    'MAX_BULK_CONTACTS': 10000,
    'EXPIRATIONS': {
        'contact_queues:double-opt-in': timedelta(days=7),
        'contact_queues:bounce-check': timedelta(hours=1),
        'contact_queues:consumed_lifetime': timedelta(days=7),
        'contact_queues:failed_lifetime': timedelta(days=7),
        'contact_lists:double-opt-in': timedelta(days=7),
        'contact_lists:bounce-check': timedelta(hours=1),
        'contact_lists:consumed_lifetime': timedelta(days=7),
        'contact_lists:failed_lifetime': timedelta(days=7)}
}

################
# Upload store #
################
UPLOAD_STORE['URL'] = 'http://munch.example.com'
UPLOAD_STORE['IMAGE_MAX_WIDTH'] = 600
UPLOAD_STORE['BACKEND'] = (
    'munch.apps.upload_store.backends.LocalFileSystemStorage')

#########
# Spamd #
#########
SPAMD_PORT = 1783

#########
# Clamd #
#########
CLAMD_PORT = 13310

###############
# Backmuncher #
###############
BACKMUNCHER['PROXYPROTO_ENABLED'] = True
