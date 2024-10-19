from flask import Flask
import os
import pytz
from datetime import datetime
import subprocess
import platform
import json

app = Flask(__name__)

@app.route('/htop')
def htop():
    try:
        full_name = "Abhinav Nair"

        # Get system username
        username = os.getlogin()

        # Get the server time in IST
        tz = pytz.timezone('Asia/Kolkata')
        server_time_ist = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S.%f')

        # Initialize top output string
        top_output_str = ""

        # Check if running on Windows or Linux
        if platform.system() == 'Windows':
            # Use PowerShell to get detailed process information
            command = "powershell -command \"Get-Process | Select-Object Id, ProcessName, CPU, WS, Handles | ConvertTo-Json\""
            top_data = subprocess.check_output(command, shell=True, text=True)
            top_output = json.loads(top_data)

            # Prepare formatted output for Windows
            top_output_str += "TOP output:\n\n"
            top_output_str += "PID\tUSER\tPR\tNI\tVIRT\tRES\tSHR\tS\tCPU\tMEM\tTIME\tCOMMAND\n"
            for proc in top_output:
                cpu_value = proc['CPU'] if proc['CPU'] is not None else "N/A"
                top_output_str += f"{proc['Id']}\t{username}\t0\t0\t{proc['WS']}\tN/A\tN/A\tN/A\t{cpu_value}\tN/A\tN/A\t{proc['ProcessName']}\n"
        else:
            # For Linux/Unix, use the top command and filter relevant columns
            top_data = subprocess.check_output("top -b -n 1 | awk 'NR>7 {print $1, $12, $9, $10, $11}'", shell=True, text=True)
            # Prepare formatted output for Linux
            top_output_str += "TOP output:\n\n"
            top_output_str += "PID\tUSER\tPR\tNI\tVIRT\tRES\tSHR\tS\tCPU\tMEM\tTIME\tCOMMAND\n"
            for line in top_data.splitlines():
                columns = line.split()
                if len(columns) >= 5:  # Ensure there are at least 5 columns
                    top_output_str += f"{columns[0]}\t{username}\t0\t0\tN/A\tN/A\tN/A\tN/A\t{columns[2]}\tN/A\tN/A\t{columns[1]}\n"

        # Return the formatted output as HTML
        return f"""
        <h1>Name: {full_name}</h1>
        <h2>User: {username}</h2>
        <h3>Server Time (IST): {server_time_ist}</h3>
        <pre>
        {top_output_str}
        </pre>
        """
    
    except Exception as e:
        # Log the error and return a friendly message
        print(f"Error: {e}")
        return "An error occurred while processing your request.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
