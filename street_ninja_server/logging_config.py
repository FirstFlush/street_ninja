import colorlog

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s%(asctime)s - %(levelname)s - %(module)s - %(message)s",
            # 'format': "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'file': {
            'format': "%(asctime)s - %(levelname)s - %(module)s - %(message)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'log.street_ninja.log',
            'formatter': 'file',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'django.utils.autoreload': {
            'handlers': ['console'],
            'level': 'WARNING',  # Suppress autoreload logs
            'propagate': False,
        },
    },
}
