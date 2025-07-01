# Task_Manager_Clone
A feature-rich Task Manager Clone built using Python (Tkinter + Matplotlib + psutil) that provides real-time system performance monitoring and process management—just like the Windows Task Manager!

🚀 Features :
🧾 Processes Tab
View all active processes with:
PID
Process Name
CPU Usage (%)
Memory Usage (%)
Option to End Tasks directly from the interface

📈 Performance Tab
Real-time metrics:
CPU usage
Memory usage
Disk usage
Network activity
Dynamic CPU usage line graph using Matplotlib
🕒 Live Auto-Refresh
Updates every 2 seconds for accurate and up-to-date information

🛠️ Tech Stack :
Python 3
Tkinter – GUI interface
psutil – System process and hardware monitoring
matplotlib – CPU usage visualization

📂 File Structure :
├── task_manager.py        # Main application code
├── README.md              # Project documentation

🧪 How to Run :
Install the required packages: pip install psutil matplotlib
Run the app: python task_manager.py

🧠 Concepts Practiced :
Process iteration and filtering
Killing processes safely
Embedding Matplotlib in Tkinter
Dynamic GUI updates with .after() method
Real-time performance monitoring
