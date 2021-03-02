FROM python:3
WORKDIR /app
ADD . /app/
RUN pip install pymysql
RUN pip install discord
RUN pip install python-dotenv
CMD [ "python", "main.py" ]