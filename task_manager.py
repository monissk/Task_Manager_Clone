import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager Clone")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        # Create a notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add tabs
        self.processes_tab = ttk.Frame(self.notebook)
        self.performance_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.processes_tab, text="Processes")
        self.notebook.add(self.performance_tab, text="Performance")

        # Initialize tabs
        self.create_processes_tab()
        self.create_performance_tab()

        # Refresh data every 2 seconds
        self.update_data()

    def create_processes_tab(self):
        # Create a treeview to display processes
        columns = ("PID", "Name", "CPU %", "Memory %")
        self.tree = ttk.Treeview(self.processes_tab, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add a button to kill a process
        self.kill_button = ttk.Button(self.processes_tab, text="End Task", command=self.kill_process)
        self.kill_button.pack(pady=10)

    def create_performance_tab(self):
        # Create a frame for performance metrics
        self.performance_frame = ttk.Frame(self.performance_tab)
        self.performance_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Add labels for CPU, memory, disk, and network usage
        self.cpu_label = ttk.Label(self.performance_frame, text="CPU Usage: 0%")
        self.cpu_label.pack(pady=5)

        self.memory_label = ttk.Label(self.performance_frame, text="Memory Usage: 0%")
        self.memory_label.pack(pady=5)

        self.disk_label = ttk.Label(self.performance_frame, text="Disk Usage: 0%")
        self.disk_label.pack(pady=5)

        self.network_label = ttk.Label(self.performance_frame, text="Network Usage: 0 bytes sent")
        self.network_label.pack(pady=5)

        # Add a real-time graph for CPU usage
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.ax.set_title("CPU Usage Over Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("CPU %")
        self.ax.grid(True)

        # Embed the graph in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.performance_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_data(self):
        # Update processes tab
        self.update_processes()

        # Update performance tab
        self.update_performance()

        # Schedule the function to run again after 2 seconds
        self.root.after(2000, self.update_data)

    def update_processes(self):
        # Clear the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch and display active processes
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                self.tree.insert("", "end", values=(
                    proc.info['pid'],
                    proc.info['name'],
                    f"{proc.info['cpu_percent']:.2f}",
                    f"{proc.info['memory_percent']:.2f}"
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def update_performance(self):
        # Update CPU, memory, disk, and network usage
        self.cpu_label.config(text=f"CPU Usage: {psutil.cpu_percent()}%")
        self.memory_label.config(text=f"Memory Usage: {psutil.virtual_memory().percent}%")
        self.disk_label.config(text=f"Disk Usage: {psutil.disk_usage('/').percent}%")
        self.network_label.config(text=f"Network Usage: {psutil.net_io_counters().bytes_sent} bytes sent")

        # Update the CPU usage graph
        if not hasattr(self, 'cpu_data'):
            self.cpu_data = []  # Initialize CPU data list

        # Append new CPU usage data
        self.cpu_data.append(psutil.cpu_percent())
        if len(self.cpu_data) > 20:  # Keep only the last 20 data points
            self.cpu_data.pop(0)

        # Clear the previous graph and plot the updated data
        self.ax.clear()
        self.ax.plot(self.cpu_data, label="CPU %")
        self.ax.set_title("CPU Usage Over Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("CPU %")
        self.ax.grid(True)
        self.ax.legend()

        # Redraw the canvas
        self.canvas.draw()

    def kill_process(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a process to kill.")
            return

        pid = int(self.tree.item(selected_item, "values")[0])
        try:
            process = psutil.Process(pid)
            process.terminate()
            messagebox.showinfo("Success", f"Process {pid} terminated successfully.")
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", f"Process {pid} no longer exists.")
        except psutil.AccessDenied:
            messagebox.showerror("Error", f"Access denied to terminate process {pid}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()