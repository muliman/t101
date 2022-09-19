FROM python:3.7-slim
RUN mkdir ./code
COPY ./src ./code
COPY ./requirements.txt ./code/requirements.txt
WORKDIR ./code
RUN pip3 install -r requirements.txt
CMD ["python", "./lab1.py"]