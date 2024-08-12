from flask import Flask, render_template
import boto3
import socket

app = Flask(__name__)


@app.route("/")
def hello_world():
    s3 = boto3.resource('s3')

    my_bucket = s3.Bucket('s3-project-001-static')
    s3_bucket = my_bucket.objects.all()
    hostname = socket.gethostname()

    return render_template('index.html', hostname=hostname, s3_bucket=s3_bucket)