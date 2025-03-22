MODE_COUNT = 0x00
MODE_TIME = 0x01

TARGET_SPECIFIED = 0x00
TARGET_FILE = 0x01

DEFAULT_UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36'
DEFAULT_COUNT = 100
DEFAULT_TIMEOUT = 10
DEFAULT_TIME = 10
DEFAULT_THREAD = 20

DEFAULT_CONFIG_LAYER4 = {
    'IP': {
        'value': '',
        'help': 'Target IP addresses.',
    },
    'Ports': {
        'value': '80',
        'help': 'Target ports.',
    },
    'Count': {
        'value': '100',
        'help': 'Count of send.',
    },
    'Time': {
        'value': '10',
        'help': 'Stop sending packet after specified time.',
    },
    'Timeout': {
        'value': '10',
        'help': 'Timeout.'
    },
    'Mode': {
        'value': '0',
        'help': 'Send mode.',
        'option': {
            MODE_COUNT: 'Send packet with specified count.',
            MODE_TIME: 'Send packet and stop after specified time.',
        }
    }
}

DEFAULT_CONFIG_WEB = {

}