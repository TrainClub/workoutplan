FROM public.ecr.aws/lambda/python:3.13
COPY main.py ./
COPY Controller/ ./Controller/
COPY utils/ ./utils/
COPY templates/ ./templates/
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
CMD [ "main.lambda_handler" ]