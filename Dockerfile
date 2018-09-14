FROM codait/max-base

# Fill in these with a link to the bucket containing the model and the model file name
ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net
ARG model_file=facial-age-estimator.tar.gz

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}
RUN tar -x -C assets/ -f assets/${model_file} -v

#opencv
RUN apt-get update && apt-get install libgtk2.0 -y

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

# Python package versions
ARG python_version=3.6.6
ARG tf_version=1.1.0
ARG keras_version=2.2.2

RUN pip install tensorflow==${tf_version} \
    flask-restplus \
    pillow \
    scipy \
    keras==${keras_version} \
    opencv-python \
    mtcnn

COPY . /workspace

EXPOSE 5000

CMD python app.py
