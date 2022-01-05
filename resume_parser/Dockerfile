FROM python:3.8

WORKDIR /app
COPY . .

RUN pip install pipenv 
RUN pipenv install --system --deploy

ENV IS_DOCKER_CONTAINER Yes

ENTRYPOINT ["python"]
CMD ["app.py"]