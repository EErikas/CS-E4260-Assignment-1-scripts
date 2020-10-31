from datetime import datetime as dt
import os
import csv
import json
import requests
import isodate
import pyyoutube
from config import yt_api_key, ip_stack_key, select_from_dir, pwd

sources_dir = os.path.join(pwd, 'sources')
data_dir = os.path.join(pwd, 'data')


def get_video_data(video_id):
    key = yt_api_key
    api = pyyoutube.Api(api_key=key)
    video = api.get_video_by_id(video_id=video_id).items[0].to_dict()
    return{
        # 'language':video.get('snippet').get('defaultAudioLanguage'),
        'date': video.get('snippet').get('publishedAt'),
        'title': video.get('snippet').get('title'),
        'views': video.get('statistics').get('viewCount'),
        'duration': isodate.parse_duration(video.get('contentDetails').get('duration')).total_seconds()
    }


def get_url_data(url_file):
    url_data = {}
    with open(os.path.join(sources_dir, url_file), 'r') as target:
        lines = target.readlines()
        for line in lines:
            line = line.replace('\n', '')
            video_id = line.split('?')[-1][2:]
            url_data.update({line: get_video_data(video_id)})
    return url_data


def get_ip_data(ip):
    access_key = ip_stack_key
    url = 'http://api.ipstack.com/{0}?access_key={1}'.format(ip, access_key)
    return requests.get(url).json()


def get_locations():
    url_data_dir = select_from_dir(data_dir)
    data_files = [foo for foo in os.listdir(
        url_data_dir) if not os.path.isdir(os.path.join(url_data_dir, foo))]

    source_file = select_from_dir(sources_dir)
    yt_url_info = get_url_data(source_file)
    locales = []
    for data_file in data_files:
        print('Getting information from {} ...'.format(data_file))
        country_info = {'location': data_file}
        with open(os.path.join(url_data_dir, data_file), 'r') as target:
            reader = csv.DictReader(target)
            urls = {}
            for row in reader:
                ip_data = get_ip_data(row['IP'])
                url = row['Url']
                ip_address_data = {
                    'IP': row['IP'],
                    'city': ip_data.get('city'),
                    'country': ip_data.get('country_name'),
                    'latitude': ip_data.get('latitude'),
                    'longitude': ip_data.get('longitude')
                }
                if url in urls.keys():
                    urls.get(url).append(ip_address_data)
                else:
                    urls.update({url: [ip_address_data]})

            url_data = [{'yt_url': key, **yt_url_info.get(key), 'locations': values}
                        for key, values in urls.items()]

        country_info.update({'urls': url_data})
        locales.append(country_info)
    return locales


if __name__ == "__main__":
    file_name = 'results {}.json'.format(
        dt.now().strftime("%m-%d-%Y_%H-%M-%S"))
    results_dir = os.path.join(pwd, 'results')
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)
    with open(os.path.join(results_dir, file_name), 'w', encoding='utf-8') as results:
        json.dump(get_locations(), results, indent=2, ensure_ascii=False)
