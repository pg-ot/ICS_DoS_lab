from flask import Flask, render_template, jsonify, request
import socket
import json

app = Flask(__name__)

def plc_request(command):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(('localhost', 5020))
        s.send(command.encode())
        response = s.recv(1024).decode()
        s.close()
        return response
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    data = plc_request('GET')
    if data:
        return jsonify(json.loads(data))
    return jsonify({'error': 'PLC connection lost'}), 503

@app.route('/api/control', methods=['POST'])
def control():
    device = request.json.get('device')
    action = request.json.get('action')
    
    if device == 'pump':
        state = 1 if action == 'start' else 0
        plc_request(f'PUMP:{state}')
    elif device == 'valve':
        state = 1 if action == 'open' else 0
        plc_request(f'VALVE:{state}')
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
