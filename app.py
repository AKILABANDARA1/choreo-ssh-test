from flask import Flask
import os

app = Flask(__name__)

def get_ngrok_ssh_info():
    log_file = "/tmp/ngrok.log"
    if not os.path.exists(log_file):
        return None

    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
        for line in reversed(lines):
            if "url=" in line and "tcp://" in line:
                tcp_url = line.split("url=")[1].strip()
                return tcp_url.replace("tcp://", "")
    except Exception as e:
        print(f"[ERROR] Failed to read ngrok.log: {e}")
        return None

@app.route("/")
def index():
    ssh_info = get_ngrok_ssh_info()
    if ssh_info is None:
        return "<h1>Waiting for Ngrok tunnel to start...</h1>"

    try:
        host, port = ssh_info.split(":")
    except ValueError:
        host, port = ssh_info, "?"

    return f"""
    <h1>SSH Tunnel Info</h1>
    <p><strong>Username:</strong> appuser</p>
    <p><strong>Password:</strong> choreo123</p>
    <p><strong>Ngrok TCP:</strong> {ssh_info}</p>
    <p><strong>SSH Command:</strong></p>
    <pre>ssh -p {port} appuser@{host}</pre>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
