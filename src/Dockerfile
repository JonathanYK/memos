# base image (python offical):
FROM python:3.8

# configure the working directory to be the main dir of the project:
WORKDIR /src

# exposing port 8081 to the host:
EXPOSE 8081

# copy all the files on that dir to the image:
COPY . .

# install dependensies from the requirements.txt:
RUN pip install -r requirements.txt

# mentioning the command to be executed when creating a container:
CMD [ "python", "./main_app.py" ]

