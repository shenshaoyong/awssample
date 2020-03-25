# 导入Flask类
from flask import Flask
from flask import request
from flask import jsonify
# 实例化，可视为固定格式
app = Flask(__name__)

# route()方法用于设定路由
@app.route('/helloworld')
def hello_world():
    return 'Hello, World!'

@app.route("/getclientip", methods=["GET"])
def getclientip ():
    ip = ''
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
#    return jsonify({'ip': request.remote_addr}), 200
    return jsonify({'ip': ip}), 200
if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5000, debug=False
    app.run(host="0.0.0.0", port=5000)
