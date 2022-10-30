from google.cloud.sql.connector import Connector
import sqlalchemy
import os

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

db_user = "mikeye5_my"
db_password = "mapleleaf"
db_name = "mikeye5_runone"
db_connection_name = "ace-study-297421:europe-west2:yeomans-database"
unix_socket = '/cloudsql/{}'.format(db_connection_name)


def open_connection():

    # try:
    conn = pymysql.connect(user=db_user, password=db_password,
                           unix_socket=unix_socket, db=db_name,
                           cursorclass=pymysql.cursors.DictCursor
                           )

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

    return get_texts("sa", "Pro")


if __name__ == '__main__':
    app.run(debug=True)

# def getconn():
#     conn = connector.connect(
#         INSTANCE_CONNECTION_NAME,
#         "pymysql",
#         user=DB_USER,
#         password=DB_PASS,
#         db=DB_NAME
#     )
#     return conn


# # create connection pool with 'creator' argument to our connection object function
# pool = sqlalchemy.create_engine(
#     "mysql+pymysql://localhost",
#     creator=getconn,
# )

# issue = "sa"
# position = "Pro"
# dbquery = "SELECT * FROM seedTexts WHERE issue='" + issue + "' AND position='" + position + "'"


# with pool.connect() as db_conn:
#     # Grab all eligibile texts
#     # query and fetch ratings table
#     results = db_conn.execute(dbquery).fetchall()

#     # show results
#     for row in results:
#         print(row)
