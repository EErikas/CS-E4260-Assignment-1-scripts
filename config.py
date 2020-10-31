import os
import json


def select_from_dir(dir):
    file_list = sorted(os.listdir(dir))
    while True:
        print('Select file to read from:')
        print(*['{0}. {1}'.format(i, file_list[i])
                for i in range(len(file_list))], sep='\n')
        index = input('Your selection: ')
        try:
            return os.path.join(dir, file_list[int(index)])
        except:
            print('Wrong id selecte, please try again!')


pwd = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(pwd, 'config.json'), 'r', encoding='utf-8') as file:
    config_data = json.load(file)

# RequestBin config:
request_bin_url = config_data['request_bin_url']
request_bin_auth = config_data['request_bin_auth']
# Youtube API config:
yt_api_key = config_data['yt_api_key']
# IP stack API config:
ip_stack_key = config_data['ip_stack_key']
