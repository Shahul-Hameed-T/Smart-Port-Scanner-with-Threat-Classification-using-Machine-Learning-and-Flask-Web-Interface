import tkinter as tk
from tkinter import ttk, messagebox
import threading
import joblib
import pandas as pd
import socket
import ipaddress
import os
import random
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import concurrent.futures

# === Constants ===
MODEL_PATH = 'port_threat_classifier_expanded.pkl'
ENCODER_PATH = 'label_encoder.pkl'

RISKY_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP", 80: "HTTP",
    110: "POP3", 135: "RPC", 137: "NetBIOS", 139: "NetBIOS", 143: "IMAP", 161: "SNMP",
    389: "LDAP", 445: "SMB", 512: "exec", 513: "login", 514: "shell", 3306: "MySQL",
    3389: "RDP", 5900: "VNC", 8080: "HTTP-Alt"
}
COMMON_PORTS = list(RISKY_PORTS.keys())
OS_MAP = {'linux': 0, 'windows': 1, 'mac': 2}

# === ML Functions ===
def generate_synthetic_dataset(num_samples=1000):
    data = []
    os_values = list(OS_MAP.values())
    risky_ports_set = set(RISKY_PORTS.keys())
    for _ in range(num_samples):
        open_ports = random.randint(1, 30)
        risky_ports = random.randint(0, min(open_ports, len(risky_ports_set)))
        os_type = random.choice(os_values)
        label = 'threat' if risky_ports >= 3 else 'safe'
        data.append({
            'open_ports': open_ports,
            'risky_ports': risky_ports,
            'os_type': os_type,
            'label': label
        })
    return pd.DataFrame(data)

def train_and_save_model():
    df = generate_synthetic_dataset()
    le = LabelEncoder()
    df["label_encoded"] = le.fit_transform(df["label"])
    X = df[["open_ports", "risky_ports", "os_type"]]
    y = df["label_encoded"]
    clf = RandomForestClassifier()
    clf.fit(X, y)
    joblib.dump(clf, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)

def load_model_and_encoder():
    if not (os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH)):
        train_and_save_model()
    clf = joblib.load(MODEL_PATH)
    le = joblib.load(ENCODER_PATH)
    return clf, le

# === Scanning Functions ===
def validate_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            if sock.connect_ex((ip, port)) == 0:
                return port
    except:
        return None
    return None

def scan_ports(ip, ports):
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda p: scan_port(ip, p), ports)
    return [port for port in results if port]

def extract_features(open_ports, os_type):
    risky_count = sum(1 for port in open_ports if port in RISKY_PORTS)
    total_ports = len(open_ports)
    return pd.DataFrame([[total_ports, risky_count, os_type]],
                        columns=['open_ports', 'risky_ports', 'os_type'])

# === GUI ===
def run_scan(ip, os_name, result_text):
    if not validate_ip(ip):
        messagebox.showerror("Invalid IP", "The IP address you entered is not valid.")
        return

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Scanning {ip}...\n")

    clf, le = load_model_and_encoder()
    os_type = OS_MAP[os_name.lower()]

    open_ports = scan_ports(ip, COMMON_PORTS)
    if not open_ports:
        result_text.insert(tk.END, "No open ports found.\n")
    else:
        result_text.insert(tk.END, "\nOpen Ports and Services:\n")
        for port in open_ports:
            service = RISKY_PORTS.get(port, "Unknown")
            result_text.insert(tk.END, f" - Port {port}: {service}\n")

    features = extract_features(open_ports, os_type)
    prediction = clf.predict(features)[0]
    label = le.inverse_transform([prediction])[0]

    status = "✅ SAFE" if label == "safe" else "⚠️ THREAT"
    result_text.insert(tk.END, f"\n[RESULT] {ip} is classified as: {status}\n")

def on_scan_click(ip_entry, os_combo, result_text):
    ip = ip_entry.get().strip()
    os_name = os_combo.get().strip().lower()
    if os_name not in OS_MAP:
        messagebox.showerror("Invalid OS", "Please select a valid OS type.")
        return

    # Run scan in a separate thread to avoid freezing the UI
    threading.Thread(target=run_scan, args=(ip, os_name, result_text), daemon=True).start()

def create_gui():
    root = tk.Tk()
    root.title("Smart Port Scanner with Threat Classification")
    root.geometry("600x500")
    root.resizable(False, False)

    ttk.Label(root, text="IP Address:").pack(pady=5)
    ip_entry = ttk.Entry(root, width=40)
    ip_entry.pack()

    ttk.Label(root, text="Target OS:").pack(pady=5)
    os_combo = ttk.Combobox(root, values=["linux", "windows", "mac"])
    os_combo.current(0)
    os_combo.pack()

    scan_btn = ttk.Button(root, text="🔍 Scan", command=lambda: on_scan_click(ip_entry, os_combo, result_text))
    scan_btn.pack(pady=10)

    result_text = tk.Text(root, wrap=tk.WORD, height=20, width=70)
    result_text.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
