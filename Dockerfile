FROM python:3.7

ADD daemon.py /

ADD requirements.txt /

ADD serverControl /

RUN pip install -r requirements.txt

# CMD ["python", "./daemon.py"]

# # ENV DockerHome = /home/walid/Scrivania/python/ServerControlPanel/serverControl

# # RUN mkdir -p $DockerHome

# # WORKDIR $DockerHome

# # ENV PYTHONDONTWRITEBYTECODE 1
# # ENV PYTHONBUFFERED 1

# # RUN pip install --upgrade pip

# # COPY . $DockerHome


# EXPOSE 8000

# ENTRYPOINT ["python", "serverControl/manage.py" ]
# CMD ["runserver"]
