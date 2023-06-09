FROM python:3-alpine
ARG DB_USER_NAME
ARG DB_PASSWORD
ENV DB_USER_NAME=$DB_USER_NAME
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_NAME=$DB_NAME
ENV DB_HOST=$DB_HOST
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./
RUN ln -sf /dev/stdout /src/app.log \
    && ln -sf /dev/stderr /src/error.log
EXPOSE 5000
ENTRYPOINT ["python3", "src/app.py"]
