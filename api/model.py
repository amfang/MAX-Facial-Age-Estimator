from flask_restplus import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage

from config import MODEL_META_DATA
from core.backend import ModelWrapper, read_still_image
import logging


api = Namespace('model', description='Model information and inference operations')

model_meta = api.model('ModelMetadata', {
    'id': fields.String(required=True, description='Model identifier'),
    'name': fields.String(required=True, description='Model name'),
    'description': fields.String(required=True, description='Model description'),
    'license': fields.String(required=False, description='Model license')
})


@api.route('/metadata')
class Model(Resource):
    @api.doc('get_metadata')
    @api.marshal_with(model_meta)
    def get(self):
        """Return the metadata associated with the model"""
        return MODEL_META_DATA


# Creating a JSON response model: https://flask-restplus.readthedocs.io/en/stable/marshalling.html#the-api-model-factory
label_prediction = api.model('LabelPrediction', {
    'age_estimation': fields.List(fields.Float(required=True, description='Estimated age for the face')),
    'face_box': fields.List(fields.Float(required=True, description='Bounding box coordinates for the face'))
})


predict_response = api.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message'),
    'predictions': fields.List(fields.Nested(label_prediction), description='Predicted age and bounding box for each detected face')
})


# Set up parser for input data (http://flask-restplus.readthedocs.io/en/stable/parsing.html)
input_parser = api.parser()
# Example parser for file input
input_parser.add_argument('image', type=FileStorage, location='files', required=True)


@api.route('/predict')
class Predict(Resource):

    model_wrapper = ModelWrapper()

    @api.doc('predict')
    @api.expect(input_parser)
    @api.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = input_parser.parse_args()
        input_data = args['image'].read()
        stillimg = read_still_image(input_data)
        preds = self.model_wrapper.predict(stillimg)

        label_preds=[]
        for res in preds:
            label_preds.append({'age_estimation':res[0]['age'],'face_box':res[0]['box']})
        result['predictions'] = label_preds
        result['status'] = 'ok'
        logging.info(label_preds)

        return result
