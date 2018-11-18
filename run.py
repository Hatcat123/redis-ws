from flask import Flask, jsonify
import redis_chrome_ws
import config
app = Flask(__name__)


@app.route('/polling_ws/', methods=['get'])
def polling_ws():
    ws = redis_chrome_ws.rpop_lpush()
    if ws is None:
        data = None
        return jsonify({"code": 404, "data": data, "message": "队列中没有值"}), 404
    else:
        data = eval(ws)
        return jsonify({"code": 200, "data": data, "message": "返回成功"}), 200


@app.route('/ws/<host>/')
def get_ws(host):
    '''
    # 获取指定host的ws值
    :param host:
    :return:
    '''
    llist = redis_chrome_ws.get_all_data()
    for i in llist:
        if i.get('ip') == host:
            return jsonify({"code": 200, "data": i.get('web_socket'), "message": "成功返回查询的ws"}), 200
    return jsonify({"code": 400, "data": None, "message": "未能找到要查询的{}".format(host)})


if __name__ == '__main__':
    app.run(port=config.PORT,host=config.HOST,debug=config.DEBUG)

