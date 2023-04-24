FROM python:3.11

RUN pip install --upgrade pip && useradd --create-home --shell /bin/bash python

USER python

WORKDIR /home/python/app

COPY --chown=python:python requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY --chown=python:python . .

ENV PATH "${PATH}:/home/python/.local/bin/"

CMD ["bash"]