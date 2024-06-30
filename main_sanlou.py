import csv
import json
import time
from datetime import datetime
import requests

url = 'https://floor.huluxia.com/message/new/list/ANDROID/4.1.8'

# 请求参数
params = {
    'platform': 2,
    'gkey': '000000',
    'app_v1ersion': '4.3.0.4',
    'versioncode': 20141495,
    'market_id': 'floor_web',
    '_key': '29727FFEF4D045DBC7A031CB658470131C78E641C975E94B4546482C6401A4F8022AA673EBDB52D56E81A90DFE4014ED0738A159FE9F48E5',
    'device_code': '[d]19e5227a-16ee-4099-96c6-63128g85e649',
    'phone_brand_type': 'VO',
    'hlx_imei': '864325056583390',
    'hlx_android_id': '005d68d578517f5a8',
    'hlx_oaid': 'ad9001122588e3585428f020f7cc1b30a105726d721e356d4416cde265fedb2e',
    'type_id': 1,
    'start': 0,
    'count': 20
}
# 设置User-Agent
headers = {
    'User-Agent': 'okhttp/3.8.1'
}

# 用于存储消息的列表
messages = []

# 首次请求不需要传递start参数
del params['start']

# 发送请求并处理响应
response = requests.get(url, params=params, headers=headers)
response.raise_for_status()  # 如果响应状态不是200，将抛出异常

data = response.json()

if data.get('code') != 403:
    output_csv_file = 'output.csv'

    with open(output_csv_file, 'w', newline='', encoding='gb18030') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Time', 'Content'])

        messages.extend(data['datas'])

        next_start = data['start']

        count = 1
        while next_start:
            time.sleep(0.2)
            params['start'] = next_start
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            new_data = response.json()
            messages.extend(new_data['datas'])
            next_start = new_data.get('start')

            if not new_data.get('more'):
                break

            for message in messages:
                message_dict = json.loads(json.dumps(message))

                create_time = datetime.fromtimestamp(message_dict['createTime'] / 1000)
                formatted_time = create_time.strftime('%Y-%m-%d %H:%M')

                content_text = message_dict['content']['text']

                writer.writerow([formatted_time, content_text])

                print(f'当前正在处理第{count}条，时间为{formatted_time}，内容是{content_text[:30]}...')
                count += 1

print('Processing complete.')
