# 🛡️ Smart Port Scanner with Threat Classification using Machine Learning and Flask

An intelligent **Port Scanning System** that not only detects open ports but also classifies their potential threat levels using a **Random Forest Classifier**.  
The system integrates **Python socket programming**, **Machine Learning**, and a **Flask Web Interface** for real-time scanning and threat prediction.

---

## 📘 Overview

Port scanning is a key cybersecurity task for identifying open and vulnerable ports in a network.  
Traditional scanners like Nmap detect open ports but do not assess the risk level automatically.  
This project bridges that gap by introducing **machine learning–based threat classification** to enhance decision-making for network administrators.

---

## ⚙️ Features

- 🔍 Scans for open ports using Python’s socket library  
- 🤖 Classifies scanned hosts as **SAFE** or **THREAT** using a Random Forest model  
- 🌐 Flask web interface for real-time input and result visualization  
- 💾 Saves trained model using `joblib` for reuse  
- 📊 Lightweight and educational — ideal for students and small organizations  

---

## 🧠 Methodology

### 1. Dataset Generation
A synthetic dataset is generated to simulate network scenarios based on:
- Number of open ports  
- Number of risky ports (like FTP, Telnet)  
- OS type  
label = "threat" if risky_ports >= 3 else "safe"

2. Model Training
A Random Forest Classifier is trained using the generated data to predict the threat level.
model = RandomForestClassifier()
model.fit(X, y)
joblib.dump(model, 'model.pkl')

3. Port Scanning
Uses Python’s socket library to detect open ports on a given IP.
if s.connect_ex((ip, port)) == 0:
    open_ports.append(port)
   
5. Threat Classification
Predictions are made based on the number of open and risky ports along with OS type.
features = [[len(open_ports), risky_count, os_code]]
prediction = model.predict(features)[0]

6. Flask Web Interface
A simple, user-friendly Flask web app lets users input an IP address and OS type and view the results instantly.
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ip = request.form["ip"]
        os = request.form["os"]
        result = run_scan(ip, os)
    return render_template("index.html", result=result)


🖥️ Project Structure
Smart-Port-Scanner/
│
├── app.py                 # Flask web app
├── model.pkl              # Trained ML model
├── dataset_generator.py   # Synthetic dataset creation
├── scanner.py             # Port scanning logic
├── templates/
│   └── index.html         # Web interface page
├── static/
│   ├── style.css
│   └── script.js
└── README.md


🧩 Technologies Used

Programming Language	->Python
Machine Learning ->	Random Forest Classifier
Web Framework ->	Flask
Libraries ->	Scikit-learn, Pandas, Socket, Joblib
Interface ->	HTML, CSS (Flask Templates)
