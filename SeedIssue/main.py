# from google.cloud.sql.connector import Connector
# import sqlalchemy
# import os

# initialize Connector object
# connector = Connector()

# function to return the database connection object

# INSTANCE_CONNECTION_NAME = '/cloudsql/{}'.format("ace-study-297421:europe-west2:yeomans-database")  # i.e demo-project:us-central1:demo-instance
# print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")
# DB_USER = "mikeye5_my"
# DB_PASS = "mapleleaf"
# DB_NAME = "mikeye5_runone"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/file.json"


# db.py
import os
import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)

# db_user = os.environ.get()
# db_password = "mapleleaf"
# db_name = "mikeye5_runone"
# db_connection_name = "ace-study-297421:europe-west2:yeomans-database"


db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# If deployed, use the local socket interface for accessing Cloud SQL
unix_socket = '/cloudsql/{}'.format(db_connection_name)


def open_connection():

    # try:
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`

    # if os.environ.get('GAE_ENV') in ['standard', 'flex']:
    conn = mysql.connect(user=db_user, password=db_password,
                         unix_socket=unix_socket, db=db_name
                         )
    # else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        # host = '127.0.0.1'
        # conn = pymysql.connect(user=db_user, password=db_password,
        #                        host=host, db=db_name
        #                        )

    # except pymysql.MySQLError as e:
    #     print(e)

    return conn


def get_texts(issue, position):

    conn = open_connection()
    with conn.cursor() as cursor:
        dbquery = "SELECT * FROM seedTexts WHERE issue='" + issue + "' AND position='" + position + "'"
        result = cursor.execute(dbquery)
        # Grab all eligibile texts
        cursor.execute(dbquery)
        sqlpull = [list(x) for x in cursor.fetchall()]
    conn.close()
    return sqlpull


@app.route('/', methods=['POST', 'GET'])
def texts():

    issue = request.args.get('issue', None)
    position = request.args.get('position', None)

    return get_texts(issue, position)


if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8080, debug=True)
    app.run(debug=True)
