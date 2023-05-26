FROM python:3-alpine
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./
EXPOSE 8080
ENTRYPOINT ["python3", "src/app.py"]
