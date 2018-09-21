# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False

# Application settings

# API metadata
API_TITLE = 'Model Asset Exchange Server'
API_DESC = 'An API for serving models'
API_VERSION = '0.1'

# default model
MODEL_NAME = 'ssrnet_3_3_3_64_1.0_1.0.h5'
FACE_NAME = 'lbpcascade_frontalface_improved.xml'
DEFAULT_MODEL_PATH = 'assets/{}'.format(MODEL_NAME)
DEFAULT_DETECTOR_PATH = 'assets/{}'.format(FACE_NAME)
MODEL_LICENSE = 'MODEL LICENSE'

MODEL_META_DATA = {
    'id': '{} MODEL ID'.format(MODEL_NAME.lower()),
    'name': '{} MODEL NAME'.format(MODEL_NAME),
    'description': '{} MODEL DESCRIPTION'.format(MODEL_NAME),
    'type': 'TYPE',
    'license': '{}'.format(MODEL_LICENSE)
}
