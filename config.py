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
MODELNAME = 'ssrnet_3_3_3_64_1.0_1.0.h5'
DEFAULT_MODEL_PATH = 'assets/{}'.format(MODELNAME)
MODEL_LICENSE = 'MIT'

MODEL_META_DATA = {
    'id': 'ssrnet',
    'name': 'SSR-Net Facial Age Estimator Model',
    'description': 'SSR-Net Facial Recognition and Age Prediction model; trained using Keras on the IMDB-WIKI dataset',
    'type': 'facial-recognition',
    'license': '{}'.format(MODEL_LICENSE)
}
