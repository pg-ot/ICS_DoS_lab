import socket
import json
import time
import threading

class PLC:
    def __init__(self):
        self.tank_level = 50.0
        self.pump_on = False
        self.valve_open = False
        self.running = True
        
    def update(self):
        if self.pump_on:
            self.tank_level = min(100.0, self.tank_level + 2.0)
        if self.valve_open:
            self.tank_level = max(0.0, self.tank_level - 1.5)
        if not self.pump_on and not self.valve_open:
            self.tank_level = max(0.0, self.tank_level - 0.1)
    
    def get_state(self):
        flow_in = 120 if self.pump_on else 0
        flow_out = 150 if (self.valve_open and self.tank_level > 0) else 0
        return {
            'tank_level': round(self.tank_level, 1),
            'pump_on': self.pump_on,
            'valve_open': self.valve_open,
            'flow_in': flow_in,
            'flow_out': flow_out
        }
    
    def set_pump(self, state):
        self.pump_on = state
    
    def set_valve(self, state):
        self.valve_open = state

def plc_server():
    plc = PLC()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5020))
    server.listen(5)
    print("[PLC] Running on port 5020")
    
    def process_loop():
        while plc.running:
            plc.update()
            time.sleep(0.5)
    
    threading.Thread(target=process_loop, daemon=True).start()
    
    while True:
        try:
            client, addr = server.accept()
            data = client.recv(1024).decode()
            
            if data.startswith('GET'):
                response = json.dumps(plc.get_state())
            elif data.startswith('PUMP'):
                state = data.split(':')[1] == '1'
                plc.set_pump(state)
                response = 'OK'
            elif data.startswith('VALVE'):
                state = data.split(':')[1] == '1'
                plc.set_valve(state)
                response = 'OK'
            else:
                response = 'ERROR'
            
            client.send(response.encode())
            client.close()
        except Exception as e:
            print(f"[PLC] Error: {e}")

if __name__ == '__main__':
    plc_server()
