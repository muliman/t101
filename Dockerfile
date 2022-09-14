FROM python:3.7-slim
WORKDIR /code
COPY /home/user/Desktop/t101/src /code
CMD ["python", "./lab1.py"]