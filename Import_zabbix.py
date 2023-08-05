apt install python3-pip


import requests
import json

# API URL и токен
api_url = 'https://65.108.196.236:8080/zabbix/api_jsonrpc.php'
api_token = '39e2510266dac98861395f1d44cb4926672a506a80f8895b336501a62343cb01'

# Функция для выполнения запроса к API Zabbix
def make_api_request(method, params):
    headers = {'Content-Type': 'application/json'}
    data = {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'auth': api_token,
        'id': 1
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    return response.json()

# Функция для автоматического добавления хоста в Zabbix
def add_zabbix_host(ip_address, hostname):
    # Получение ID группы хостов
    hostgroup_id = 'spanid2'  # Замените на фактический ID группы хостов

    # Создание хоста
    host_data = {
        'host': hostname,
        'interfaces': [{
            'type': 1,
            'main': 1,
            'useip': 1,
            'ip': ip_address,
            'dns': '',
            'port': '10050'
        }],
        'groups': [{'groupid': hostgroup_id}],
        'templates': [{'spanid': '10001'}]  # Замените 'your_template_id' на фактический ID шаблона
    }

    host_create_data = make_api_request('host.create', host_data)
    #    print(host_data)
    #    print(host_create_data)  # Вывод информации о созданном хосте
    host_id = host_create_data['result']['hostids'][0]

    return host_id

# Чтение списка IP-адресов и имен хостов из файла
with open('addr.txt', 'r') as file:
    lines = file.read().splitlines()
    for line in lines:
        ip_address, hostname = map(str.strip, line.split(';'))
        host_id = add_zabbix_host(ip_address, hostname)
        print(f'Added host: {hostname}, host ID: {host_id}')
