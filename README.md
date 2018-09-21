# IBM Code Model Asset Exchange:Age Estimation with SSR-Net

The SSR-Net gives Age Estimation from giving an image or video. The model first detects human face, then automatically generate feature vector to represent every detected human face.  The model takes a coarse-to-fine strategy to perform multi-class classification and regression for age estimatation. The output of the model provides gender, age, and also bounding boxes of a given image or video. 

The model is based on the SSR-Net model. The model files are hosted on IBM Cloud Object Storage. The code in this repository deploys the model as a web service in a Docker container. This repository was developed as part of the IBM Code Model Asset Exchange.

## Model Metadata

## Model Metadata
| Domain | Application | Industry  | Framework | Training Data | Input Data Format |
| ------------- | --------  | -------- | --------- | --------- | -------------- |
| Vision | Age Estimation | General | Keras & TensorFlow | [IMDB-WIKI Dataset](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/) | Image(PNG/JPG) |


## Prerequisites:

* You will need Docker installed. Follow the [installation instructions](https://docs.docker.com/install/) for your
system.
* The minimum recommended resources for this model is 2GB Memory and 1 CPU.

## References:

* T.-Y. Yang, Y.-H. Huang, Y.-Y. Lin, P.-C. Hsiu, and Y.-Y. Chuang. SSR-Net: A Compact Soft Stagewise Regression Network for Age Estimation. IJCAI 2018.


## Licenses

| Component | License | Link  |
| ------------- | --------  | -------- |
| This repository | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](LICENSE) |
| Model Weights | [MIT](https://opensource.org/licenses/MIT) | [LICENSE](https://https://github.com/shamangary/SSR-Net/blob/master/LICENSE) |
| Model Code (3rd party) | [MIT](https://opensource.org/licenses/MIT) | [LICENSE](https://github.com/shamangary/SSR-Net/blob/master/LICENSE) |
| Test assets | Various | [Asset README](assets/README.md) |

## Pre-requisites:

* `docker`: The [Docker](https://www.docker.com/) command-line interface. Follow the [installation instructions](https://docs.docker.com/install/) for your system.
* The minimum recommended resources for this model is [Necessary GB] Memory and [Necessary CPUs] CPUs.

# Steps

1. [Deploy from Docker Hub](#deploy-from-docker-hub)
2. [Run Locally](#run-locally)

## Deploy from Docker Hub

To run the docker image, which automatically starts the model serving API, run:

```
$ docker run -it -p 5000:5000 codait/max-facial-age-estimator
```

This will pull a pre-built image from Docker Hub (or use an existing image if already cached locally) and run it.
If you'd rather checkout and build the model locally you can follow the [run locally](#run-locally) steps below.

## Run Locally

1. [Build the Model](#1-build-the-model)
2. [Deploy the Model](#2-deploy-the-model)
3. [Use the Model](#3-use-the-model)
4. [Development](#4-development)
5. [Clean Up](#5-clean-up)


### 1. Build the Model

Clone this repository locally. In a terminal, run the following command:

```
$ git clone https://github.com/IBM/MAX-Facial-Age-Estimator.git
```

Change directory into the repository base folder:

```
$ cd MAX-Facial-Age-Estimator
```

To build the docker image locally, run:

```
$ docker build -t max-facial-age-estimator .
```

All required model assets will be downloaded during the build process. _Note_ that currently this docker image is CPU only (we will add support for GPU images later).



### 2. Deploy the Model

To run the docker image, which automatically starts the model serving API, run:

```
$ docker run -it -p 5000:5000 max-facial-age-estimator
```

### 3. Use the Model
The API server automatically generates an interactive Swagger documentation page. Go to http://localhost:5000 to load it. From there you can explore the API and also create test requests. Use the model/predict endpoint to load a test image (you can use one of the test images from the assets folder) and get predicted labels for the image from the API


### 4. Development

To run the Flask API app in debug mode, edit `config.py` to set `DEBUG = True` under the application settings. You will then need to rebuild the docker image (see [step 1](#1-build-the-model)).

### 5. Cleanup

To stop the Docker container, type `CTRL` + `C` in your terminal.