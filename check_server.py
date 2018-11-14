import requests
import config
import redis_chrome_ws

ws_list = config.SERVER_LIST
import time


def get_all_data():
    datalist = []
    for i in map(lambda x: eval(x), redis_chrome_ws.lrange()):
        datalist.append(i)
    return datalist


def get_all_value():
    key_list = []
    for i in get_all_data():
        a = list(i.values())[0]
        key_list.append(a)
    return key_list


def save_ws(ip):
    try:
        data = requests.get(url='http://{}:9222/json/version'.format(ip)).json()['webSocketDebuggerUrl']
        if ip not in get_all_value():
            print("添加新WS服务{}:{}".format(ip, data))
            redis_chrome_ws.lpush({"ip": ip, "web_socket": data})
        else:
            for k, i in enumerate(get_all_data()):
                if i.get("web_socket") == data:
                    print('{} 服务地址未改变'.format(ip))
                else:
                    if str(ip) == i.get("ip"):
                        print('服务地址改变为{}'.format(data))
                        redis_chrome_ws.lset(k, {"ip": ip, "web_socket": data})
                    else:
                        pass
    except:
        print('{}服务网络链接超时'.format(ip))


while 1:
    for i in ws_list:
        save_ws(i['host'])
    time.sleep(config.SLEEP_TIME)
