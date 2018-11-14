from flask import Flask, jsonify
import redis_chrome_ws

app = Flask(__name__)


@app.route('/ws/', methods=['get'])
def get_ws():
    ws = redis_chrome_ws.rpop_lpush()
    if ws is None:
        data = None
        return jsonify({"code": 404, "data": data, "message": "队列中没有值"}), 404
    else:
        data = eval(ws)
        return jsonify({"code": 200, "data": data, "message": "返回成功"}), 200


if __name__ == '__main__':
    app.run(port=6000)
