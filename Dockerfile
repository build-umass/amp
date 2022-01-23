FROM public.ecr.aws/lambda/python:3.9

# Copy function code
COPY model_trainer.py resume.pdf app.py ${LAMBDA_TASK_ROOT}

COPY ./assests ${LAMBDA_TASK_ROOT}/assests
COPY ./configs ${LAMBDA_TASK_ROOT}/configs
# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN  python -m spacy download en_core_web_sm

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
