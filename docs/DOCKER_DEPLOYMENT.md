# Docker Deployment: Iris Classifier

## Overview

The Docker image contains a trained Iris classifier and a small HTTP prediction
service. The multi-stage build creates the training data and model in its
builder stage, then copies only the Python virtual environment, model
artifacts, and serving script into the runtime image. The dataset is generated
from scikit-learn's bundled Iris dataset during image build, so the build does
not depend on ignored or untracked local data files.

## Build and run

From the repository root, build the image:

```powershell
docker build -t iris-classifier:v1 .
```

Start the container:

```powershell
docker run -d --name iris-classifier-container -p 8000:8000 iris-classifier:v1
```

Check its status and health:

```powershell
docker ps
docker inspect --format='{{.State.Health.Status}}' iris-classifier-container
```

The health check polls `GET /health` every 30 seconds, with a five-second
timeout, a ten-second startup period, and three retries.

## HTTP endpoints

### Health

```powershell
curl.exe http://localhost:8000/health
```

Expected response:

```json
{"status":"healthy"}
```

### Prediction

The prediction endpoint accepts the four original measurements and the three
numeric engineered features:

```powershell
curl.exe -X POST http://localhost:8000/predict `
  -H "Content-Type: application/json" `
  -d '{\"sepal length (cm)\":5.1,\"sepal width (cm)\":3.5,\"petal length (cm)\":1.4,\"petal width (cm)\":0.2,\"sepal_area\":17.85,\"petal_area\":0.28,\"sepal_to_petal_length_ratio\":3.642857}'
```

A successful response contains a species prediction and class probabilities.
Malformed JSON, non-finite or non-numeric feature values, and missing features
are rejected with HTTP 400. Requests to unknown paths return HTTP 404.

## Image design

`Dockerfile` uses Python 3.11 slim images for both stages. The builder installs
the pinned dependencies from `requirements-serving.txt`, runs the existing
collection, preprocessing, and feature-engineering scripts, then trains and
saves the classifier and label encoder. The runtime stage copies only those
artifacts and the serving environment, runs as a non-root user, and listens on
port 8000. `.dockerignore` excludes local state and data; all build inputs are
generated or copied explicitly during the builder stage.

Inspect the final image size and layers with:

```powershell
docker images iris-classifier
docker history iris-classifier:v1
```

The build is multi-stage to keep training-time scripts and data out of the
runtime image. The exact image size depends on the pinned Python and
scikit-learn dependencies; use the `docker images` output rather than assuming
a particular size.

## Publish to Docker Hub

The `docker-publish.yml` workflow publishes
`beherelokesh12345/iris-classifier:v1` when manually run from `main`. Before
running it, create a Docker Hub access token with read/write permissions and
add these repository secrets under **Settings → Secrets and variables →
Actions**:

- `DOCKERHUB_USERNAME`: your Docker Hub login username.
- `DOCKERHUB_TOKEN`: the Docker Hub access token (do not use or commit your
  account password).

Then open **Actions → Publish Iris classifier to Docker Hub → Run workflow**,
select `main`, and start the workflow. A successful run builds the image and
pushes the `v1` tag. Pull it with:

```powershell
docker pull beherelokesh12345/iris-classifier:v1
```

The publishing workflow is separate from pull-request checks and refuses to
publish from a branch other than `main`.

The GitHub Actions `docker-container-check` job also builds the image on an
Ubuntu runner and verifies container health, the health endpoint, a valid
prediction and its probabilities, rejection of a request with missing
features, server logs, and cached layers on a second build. Its job logs show
the image size and first/second build output. This runner-based check is useful
when Docker is not installed locally; it does not report the size of an image
built on a developer's own machine.

## Logs and cleanup

```powershell
docker logs iris-classifier-container
docker stop iris-classifier-container
docker rm iris-classifier-container
```

## Verification status

The image build, endpoint behavior, and Docker layer cache are exercised in
the `docker-container-check` GitHub Actions job. To record a local image size
or verify a local Docker Engine, repeat the commands above on a machine with
Docker Desktop or Docker Engine installed.
