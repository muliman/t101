FROM python:3.7-slim
RUN mkdir ./code
COPY ./src ./code
WORKDIR ./code
CMD ["python", "./lab1.py"]