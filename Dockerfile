FROM python:3.8.1-slim

ENV PROJECT_ROOT=/app
ENV SRC_ROOT=$PROJECT_ROOT/src

ENV PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

ENV BUILD_PACKAGES \
    libev-dev \
    git \
    gcc \
    wget \
    gfortran \
    libpng-dev \
    libc-dev \
    musl-dev \
    python3-dev \
    libffi-dev


RUN mkdir $PROJECT_ROOT/

COPY ./Pipfile ./Pipfile.lock $PROJECT_ROOT/

WORKDIR $PROJECT_ROOT

RUN pip install --upgrade pip wheel pipenv \
    && apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends $BUILD_PACKAGES \
    && apt-get install -y --no-install-recommends curl \
    && apt-get install -y --no-install-recommends locales \
    && apt-get install -y --no-install-recommends ffmpeg libavcodec-extra \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && pipenv install --deploy --system --dev \
    && apt-get remove -y $BUILD_PACKAGES && apt-get autoremove -y

COPY . $PROJECT_ROOT

WORKDIR $SRC_ROOT

CMD ["python", "./run.py"]
