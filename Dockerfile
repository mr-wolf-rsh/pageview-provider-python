FROM python:3.9

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

COPY /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /pageviewprovider

COPY . .

CMD ["/.venv/bin/python", "pageviewprovider"]