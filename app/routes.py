from flask import render_template
from app import app

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
import local_settings as settings

try:
    client = InfluxDBClient(host='127.0.0.1',
                        port=8086,
                        username=settings.user,
                        password=settings.password,
                        database=settings.dbname)
except:
    client = None


@app.route('/')
def index():
    try:
        resp = client.query("SELECT temperature FROM ruuvi WHERE sensor='Balcony' GROUP BY * ORDER BY DESC LIMIT 1").raw
        outside_temp = resp.raw['series'][0]['values'][0][1]  # wow this is bad...
    # except InfluxDBClientError:
    except:
        outside_temp = None

    return render_template('index.html', outside_temp=outside_temp)
