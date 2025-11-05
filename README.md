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



🧩 Technologies Used

Programming Language	->Python
Machine Learning ->	Random Forest Classifier
Web Framework ->	Flask
Libraries ->	Scikit-learn, Pandas, Socket, Joblib
Interface ->	HTML, CSS (Flask Templates)
