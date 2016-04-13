import logging

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(name)-10s %(levelname)-10s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'parser': {
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
