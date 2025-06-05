from flask import Flask
import time
import os

app = Flask(__name__)

def get_ngrok_ssh_info():
    # Wait for ngrok to start
    time.sleep(5)
    try:
        with open("ngrok.log", "r") as f:
            lines = f.readlines()
        for line in lines:
            if "url=" in line and "tcp://" in line:
                tcp_url = line.split("url=")[1].strip()
                return tcp_url.replace("tcp://", "")
    except Exception as e:
        return f"Error: {e}"
    return "Waiting for Ngrok..."

@app.route("/")
def index():
    ssh_info = get_ngrok_ssh_info()
    return f"""
    <h1>SSH Tunnel Information</h1>
    <p><strong>Username:</strong> appuser</p>
    <p><strong>Password:</strong> choreo123</p>
    <p><strong>Connect using:</strong></p>
    <pre>ssh -p {ssh_info.split(':')[1]} appuser@{ssh_info.split(':')[0]}</pre>
    <p>Ngrok Tunnel: <code>{ssh_info}</code></p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
