import os
from datetime import datetime

from botocore.exceptions import ClientError
from flask import Flask, render_template, request, redirect, url_for
import boto3
import socket
import psycopg2
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


ssm = boto3.client('ssm', region_name='sa-east-1')

# So bad, but need to make a fast deploy
DB_USER = "postgres"
DB_NAME = "postgres"
DB_PASSWORD = "ABCD1234abcd#"
DB_ENDPOINT = ssm.get_parameter(Name='db-endpoint').get('Parameter').get('Value')
DB_PORT = "5432"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['POST', 'GET'])
def index():

    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')

    bucket_name = 's3-project-001-static'
    con = psycopg2.connect(host=DB_ENDPOINT, database=DB_NAME, port=DB_PORT,
                           user=DB_USER, password=DB_PASSWORD)

    if not os.path.exists('tmp_img'):
        os.mkdir('tmp_img')

    if request.method == 'POST':
        req = request.form.to_dict()
        sql_insert = f'INSERT INTO public.users ("name") VALUES(%s)'
        try:
            cur = con.cursor()
            cur.execute(sql_insert, (req.get('name'),))
            con.commit()
        except Exception as e:
            print(e)
        con.close()

        if 'file_img' in request.files:
            file = request.files['file_img']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('tmp_img', filename))

                try:
                    s3_client.upload_file(os.path.join('tmp_img', filename), bucket_name, 'images/' + filename)
                    os.remove(os.path.join('tmp_img', filename))
                except ClientError as e:
                    print(e)

        return redirect(url_for('index'))

    cur = con.cursor()

    cur.execute('SELECT * FROM public.users')
    users = cur.fetchall()

    con.close()

    my_bucket = s3.Bucket(bucket_name)
    s3_bucket = my_bucket.objects.all()
    hostname = socket.gethostname()

    return render_template('index.html', hostname=hostname, s3_bucket=s3_bucket, time=datetime.now(), users=users)
