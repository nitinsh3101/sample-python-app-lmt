FROM python:3-alpine
# ARG DB_USER_NAME
# ARG DB_PASSWORD
# ARG DB_NAME
# ARG DB_HOST
# ENV DB_USER_NAME=$DB_USER_NAME
# ENV DB_PASSWORD=$DB_PASSWORD
# ENV DB_NAME=$DB_NAME
# ENV DB_HOST=$DB_HOST
ENV DB_USER_NAME=/run/secrets/rds-credentials/DB_USER_NAME
ENV DB_PASSWORD=/run/secrets/rds-credentials/DB_PASSWORD
ENV DB_NAME=/run/secrets/rds-credentials/DB_NAME
ENV DB_HOST=/run/secrets/rds-credentials/DB_HOST

WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./
RUN ln -sf /dev/stdout /src/app.log \
    && ln -sf /dev/stderr /src/error.log
EXPOSE 5000
ENTRYPOINT ["python3", "src/app.py"]
