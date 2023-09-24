FROM python:3.10
COPY . /code
WORKDIR /code
RUN pip install pip  --upgrade
RUN apt-get update && apt-get install -y python3
RUN pip install -r requirements.txt && ls
RUN chmod 777 script.sh
CMD ./script.sh