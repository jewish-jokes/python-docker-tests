FROM python:3.8

RUN pip install --upgrade pip && useradd --create-home --shell /bin/bash python

USER python

WORKDIR /home/python/app

COPY --chown=python:python requirements-prod.txt requirements-prod.txt

RUN pip install -r requirements-prod.txt

ENV PYTHONPATH "${PYTHONPATH}:/home/python/app"

COPY --chown=python:python . .

CMD ["bash"]