# Base image
FROM rahulvbrahmal/python-with-talib:latest

# # Maintainer Info
LABEL maintainer="Rahul Brahmal <rahul@imbue.dev>"

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

# # install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install black

# # copy project
COPY . .

EXPOSE 8000

CMD ["sh", "docker-entrypoint.sh"] 