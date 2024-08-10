FROM python:3.10

WORKDIR /Workspace
COPY requirements.txt ./requirements/requirements.txt

RUN git clone -b feat/add-kedro-framework https://github.com/julionevadod/ClickbaitDetector.git repos/ClickbaitDetector

RUN pip install "cython<3.0.0" wheel
RUN pip install "pyyaml==5.4.1" --no-build-isolation
RUN pip install -r ./requirements/requirements.txt
RUN pip install repos/ClickbaitDetector
RUN pip install -r repos/ClickbaitDetector/requirements.txt
RUN pip install -r repos/ClickbaitDetector/kedro/clickbait-detector-kedro/requirements.txt
RUN pip install aiohttp
RUN pip install requests

WORKDIR repos/ClickbaitDetector/kedro/clickbait-detector-kedro
