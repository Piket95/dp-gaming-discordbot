FROM python:3
WORKDIR /app
ADD . /app/
RUN pip install pymysql
RUN pip install discord
CMD [ "python", "main.py" ]