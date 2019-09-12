FROM python:3.6-jessie
COPY $PWD /bistro/
WORKDIR /bistro/

RUN pip install -r requirements.txt