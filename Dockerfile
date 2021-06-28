FROM python:3.8
ADD  ./requirements.txt ./
RUN  pip3 install -r requirements.txt
COPY . /app
WORKDIR /app

EXPOSE 5002
CMD ["python", "./app.py"]