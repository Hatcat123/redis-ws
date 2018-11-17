import redis
import config

connect = redis.Redis(host=config.REIDS_HOST, port=config.REIDS_PORT, db=config.REIDS_DB)


def lpush(ws):
    return connect.lpush(config.REIDS_DB3_ROW, ws)


def rpop():
    return connect.rpop(config.REIDS_DB3_ROW)


def rpop_lpush():
    # 右边取出后左边插入  原子性安全的队列
    return connect.rpoplpush(config.REIDS_DB3_ROW, config.REIDS_DB3_ROW)

def flushall():
    return connect.flushall()

def lrange():
    return connect.lrange(config.REIDS_DB3_ROW, 0, -1)

def lset(k,data):
    return connect.lset(config.REIDS_DB3_ROW,k,data)

def get_len():
    return connect.llen(config.REIDS_DB3_ROW)


def get_all_data():
    datalist = []
    for i in map(lambda x: eval(x), connect.lrange(config.REIDS_DB3_ROW, 0, -1)):
        datalist.append(i)
    return datalist


def get_all_value():
    key_list = []
    for i in get_all_data():
        a = list(i.values())[0]
        key_list.append(a)
    return key_list

