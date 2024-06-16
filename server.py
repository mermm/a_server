from flask import Flask, request, jsonify
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app)
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/logs', methods=['GET'])
def get_logs():
    severity = request.args.get('severity')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    logs = []
    for key in r.scan_iter("log:*"):
        log = r.hgetall(key)
        log = {k.decode('utf-8'): v.decode('utf-8') for k, v in log.items()}
        
        if severity and log["severity"] != severity:
            continue
        if start_date and log["date"] < start_date:
            continue
        if end_date and log["date"] > end_date:
            continue

        logs.append(log)

    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
