FROM python:2.7
ADD . /src
WORKDIR /src
CMD source bin/secrets.sh
RUN pip install -r requirements.txt