![model-simulator logo](.github/assets/images/model-simulator-logo.png)

# model-simulator

[![CircleCI](https://circleci.com/gh/intuit/model-simulator/tree/main.svg?style=svg)](https://circleci.com/gh/intuit/model-simulator/tree/main)

The main purpose of `model-sim` is to serve as a placeholder model to enable testing other tools and
workflows. It is a Docker image that can be run locally and on AWS SageMaker. It simulates varying
response times, returning error codes, reading artifacts, logging messages, and other model
behaviors.

This repo started with the
[scikit_bring_your_own](https://github.com/aws/amazon-sagemaker-examples/tree/master/advanced_functionality/scikit_bring_your_own)
example, but has modified `predictor.py` to handle requests as specified below.

# Usage

## Building and Testing on Local

### Build Locally

Clone the repo:
```sh
git clone https://github.intuit.com/data-mlplatform/model-sim-public.git # TODO: replace with public location
cd model-sim
```

Ensure the `serve` file is executable:
```sh
chmod +x model/serve
```

Build docker image:
```sh
docker build -t model-sim .
```

### Test Locally
```sh
docker run -v $(pwd)/data:/opt/ml/model -p 8080:8080 --rm model-sim:latest serve
```
- The data folder is mounted at `/opt/ml/model` to match where SageMaker will later be mounting the
  `model.tar.gz` file below.
- The service is now running at http://localhost:8080/invocations

```sh
curl --data-binary @input_data.json -H "Content-Type: application/json" -v http://localhost:8080/invocations
```
- where `input_data.json` is a file like the following sample request.

#### Sample Request
```json
{
    "sleep_seconds" : 1.500,
    "status" : 200,
    "file_path" : "1k_characters.txt",
    "message" : "hello world"
}
```
- `sleep_seconds`: Number of seconds to sleep, to simulate response time.  Optional.  Default is 0.
- `status`: HTTP status code to return, to simulate various error codes like 400, 500, etc.  Optional.  Default is 200.
- `file_path`: Name of file under /opt/ml/model to be read.  See files under `data` directory.  Could use large files to simulate large response sizes.  Optional.  Default is empty string.
- `message`:  Any string value.  Could use large messages to simulate large request sizes.  Optional.  Default is empty string.
- `exception`: Any string value.  Raise an exception with the given string, instead of returning the otherwise expected response and status.  Optional.  Default is to skip over raising an exception.
- `empty`: Boolean. If true, overrides any other settings here and returns empty string as response body.  Optional.  Default is false.

#### Sample Response
```json
{
    "echo": {
        "file_path": "1k_characters.txt",
        "message": "hello world",
        "sleep_seconds": 1.5,
        "status": 200
    },
    "file_contents": "1000m ipsum dolor sit amet, consectetur adipiscing elit. Phasellus quis sapien sem. Pellentesque rutrum rhoncus lorem, pretium cursus massa aliquet a. Curabitur egestas neque nunc, nec vehicula quam congue id. Mauris feugiat pharetra diam, non sagittis ante tincidunt vitae. Duis enim odio, gravida a mattis et, condimentum sit amet nunc. In tempus quis felis quis scelerisque. Aenean malesuada diam lectus, congue lacinia lacus porttitor id. Pellentesque eu tempor nunc. Cras et semper enim. Praesent sed dolor a nulla molestie fermentum a a enim. Maecenas erat tellus, adipiscing eget massa eu, varius placerat nunc. Morbi eros nunc, consequat quis velit at, pulvinar vulputate risus. Quisque velit tortor, posuere sed molestie at, molestie in risus. Pellentesque pellentesque lobortis nibh, nec hendrerit dolor adipiscing eu.Nunc vel ligula imperdiet, feugiat risus in, viverra metus. Etiam tempor velit in quam facilisis hendrerit. Pellentesque volutpat sollicitudin tortor at consectetur nulEND.\n",
    "file_path": "1k_characters.txt",
    "message": "hello world",
    "sleep_seconds": 1.5,
    "status": 200,
    "version": "v1.3b"
}
```
- The response includes the parameters from the request, plus:
- `file_contents`: the contents of given file, if provided.

#### Sample `standard out` (would be sent by SageMaker to CloudWatch)
```
Starting the inference server with 5 workers.
[2021-04-24 06:31:59 +0000] [9] [INFO] Starting gunicorn 20.1.0
[2021-04-24 06:31:59 +0000] [9] [INFO] Listening at: unix:/tmp/gunicorn.sock (9)
[2021-04-24 06:31:59 +0000] [9] [INFO] Using worker: sync
[2021-04-24 06:31:59 +0000] [13] [INFO] Booting worker with pid: 13
[2021-04-24 06:31:59 +0000] [14] [INFO] Booting worker with pid: 14
[2021-04-24 06:31:59 +0000] [15] [INFO] Booting worker with pid: 15
[2021-04-24 06:32:00 +0000] [17] [INFO] Booting worker with pid: 17
[2021-04-24 06:32:00 +0000] [18] [INFO] Booting worker with pid: 18
request.data: b'{\n    "sleep_seconds" : 1.500,\n    "status" : 200,\n    "file_path" : "1k_characters.txt",\n    "message" : "hello world"\n}\n'
request_dict: {'sleep_seconds': 1.5, 'status': 200, 'file_path': '1k_characters.txt', 'message': 'hello world'}
About to sleep 1.5 seconds
Return status 200 and response {"echo": {"file_path": "1k_characters.txt", "message": "hello world", "sleep_seconds": 1.5, "status": 200}, "file_contents": "1000m ipsum dolor sit amet, consectetur adipiscing elit. Phasellus quis sapien sem. Pellentesque rutrum rhoncus lorem, pretium cursus massa aliquet a. Curabitur egestas neque nunc, nec vehicula quam congue id. Mauris feugiat pharetra diam, non sagittis ante tincidunt vitae. Duis enim odio, gravida a mattis et, condimentum sit amet nunc. In tempus quis felis quis scelerisque. Aenean malesuada diam lectus, congue lacinia lacus porttitor id. Pellentesque eu tempor nunc. Cras et semper enim. Praesent sed dolor a nulla molestie fermentum a a enim. Maecenas erat tellus, adipiscing eget massa eu, varius placerat nunc. Morbi eros nunc, consequat quis velit at, pulvinar vulputate risus. Quisque velit tortor, posuere sed molestie at, molestie in risus. Pellentesque pellentesque lobortis nibh, nec hendrerit dolor adipiscing eu.Nunc vel ligula imperdiet, feugiat risus in, viverra metus. Etiam tempor velit in quam facilisis hendrerit. Pellentesque volutpat sollicitudin tortor at consectetur nulEND.\n", "file_path": "1k_characters.txt", "message": "hello world", "sleep_seconds": 1.5, "status": 200, "version": "v1.3b"}
172.17.0.1 - - [24/Apr/2021:06:32:08 +0000] "POST /invocations HTTP/1.1" 200 1247 "-" "curl/7.54.0"
```

## Deploying and Testing on Amazon SageMaker

Now that the build and local tests are passing, the next step is to deploy to Amazon SageMaker. For
the examples below, `111111111111` represents your AWS Account number.

### Publish model.tar.gz file to S3

For deployment to SageMaker, the contents of the data folder need to be packaged and pushed to an S3
location.

- Create the tar.gz file
```sh
cd data
tar -zcvf model.tar.gz *
```

- Upload the model.tar.gz file to some S3 location. For example:
```sh
aws s3 cp model.tar.gz s3://your-bucket-name-here/model-sim/1-0/model.tar.gz
```

### Publish Docker image to ECR

- AWS Console > Elastic Container Registry > Repositories > Create Repository
- Repository name: `111111111111.dkr.ecr.us-west-2.amazonaws.com/model-sim`
- Push to repository:
```sh
aws ecr get-login
docker login -u AWS -p ... https://111111111111.dkr.ecr.us-west-2.amazonaws.com
docker tag model-sim:latest 111111111111.dkr.ecr.us-west-2.amazonaws.com/model-sim:latest
docker push 111111111111.dkr.ecr.us-west-2.amazonaws.com/model-sim:latest
```

### Set up SageMaker Endpoint

#### Create model

- AWS Console > Amazon SageMaker > Inference > Models
- Model name: `model-sim`
- IAM role: new role
- Location of inference code image: `111111111111.dkr.ecr.us-west-2.amazonaws.com/model-sim:latest`
- Location of model artifacts: `s3://your-bucket-name-here/model-sim/1-0/model.tar.gz`

#### Create endpoint config

- AWS Console > Amazon SageMaker > Inference > Endpoint configurations
- Endpoint configuration name: `LEARNING-model-sim-1-0`
- Production variants: add `model-sim` model created above
- Set instance type: `ml.t2.medium` (for testing)

#### Create endpoint

- AWS Console > Amazon SageMaker > Inference > Endpoints
- Endpoint name: `LEARNING-model-sim-1`
- Endpoint configuration: the one created above
- Endpoint will be in `Creating` status. Wait a few minutes until endpoint reaches `InService`
  status.

### Test SageMaker Endpoint

One option for sending a request to the SageMaker endpoint is using the AWS CLI:
```
aws sagemaker-runtime invoke-endpoint --endpoint-name LEARNING-model-sim-1 --body '{"data":"hello"}' outfile.txt
```

The output from the command looks like:
```
{
    "ContentType": "application/json",
    "InvokedProductionVariant": "variant-name-1"
}
```
and the content of the `outfile.txt` looks like:
```
{
    "echo": {
        "data": "hello"
    },
    "file_contents": "",
    "file_path": "",
    "message": [],
    "sleep_seconds": 0,
    "status": 200,
    "version": "v1.3b"
}
```

Another option is to make an HTTP request directly to the endpoint:
https://runtime.sagemaker.us-west-2.amazonaws.com/endpoints/LEARNING-model-sim-1/invocations
but this requires setting certain headers.

For more details, see:
- [SageMaker InvokeEndpoint API](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_runtime_InvokeEndpoint.html)
- [AWS Signature Version 4](https://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html)
- [Example call including headers](https://github.intuit.com/data-mlplatform/sagemaker-gatling/blob/master/src/test/scala/SageMaker.scala#L84)

For load testing the endpoint using Gatling to make HTTP requests, see:
- [sagemaker-gatling](https://github.intuit.com/data-mlplatform/sagemaker-gatling)

# Development

TODO:
- Update Jenkinsfile to post to Docker Hub

# Contributing

Feel free to open an [issue](TODO) or [pull request](TODO)!

Make sure to read our [code of conduct](CODE_OF_CONDUCT.md).


# License

This project is licensed under the terms of the [Apache License 2.0](LICENSE).

# References
- [Use Your Own Inference Code with Hosting Services](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-inference-code.html):
  This page describes how Amazon SageMaker interacts with your Docker container and how it should
  respond.
- [Example Bring Your Own Container](https://github.com/aws/amazon-sagemaker-examples/tree/master/advanced_functionality/scikit_bring_your_own):
  Sample code used as a starting point for this repo.
