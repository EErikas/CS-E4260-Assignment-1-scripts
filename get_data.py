import http.client
import json
import os
from datetime import datetime as dt
import requests
from config import request_bin_url, request_bin_auth

conn = http.client.HTTPSConnection('api.pipedream.com')
conn.request("GET", request_bin_url, '', {
    'Authorization': request_bin_auth,
})

res = conn.getresponse()
data = res.read()

response = json.loads(data.decode("utf-8"))

pwd = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(pwd, 'data')

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

folder_name = 'data_{}'.format(
    dt.now().strftime("%m-%d-%Y_%H-%M-%S"))

data_folder = os.path.join(data_dir, folder_name)
os.mkdir(data_folder)

for foo in response['data']:
    data = foo['event']
    file_name = data['headers'].get('vantage-point', 'NA') + '.csv'
    with open(os.path.join(data_folder, file_name), 'w', encoding='utf-8') as file:
        body = data['bodyRaw'].split(',')
        step = 29
        csv_lines = [','.join(body[i:i+step]) +
                     '\n' for i in range(0, len(body), step)]
        file.writelines(csv_lines)
