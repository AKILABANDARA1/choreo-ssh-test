from flask import Flask
import os
import traceback

app = Flask(__name__)

# Global error log list (in-memory)
error_logs = []

def log_error(msg):
    print(msg)  # also print to container logs
    error_logs.append(msg)

def get_ngrok_ssh_info():
    log_file = "/tmp/ngrok.log"
    if not os.path.exists(log_file):
        log_error(f"Log file {log_file} does not exist yet.")
        return None

    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
        for line in reversed(lines):
            if "url=" in line and "tcp://" in line:
                tcp_url = line.split("url=")[1].strip()
                return tcp_url.replace("tcp://", "")
        log_error("No ngrok tcp url found in log file.")
        return None
    except Exception as e:
        tb = traceback.format_exc()
        log_error(f"Exception reading ngrok log file:\n{tb}")
        return None

@app.route("/")
def index():
    ssh_info = get_ngrok_ssh_info()

    error_section = ""
    if error_logs:
        error_section = "<h2>Errors:</h2><pre style='color: red; background:#fee; padding:10px;'>" + \
                        "\n".join(error_logs[-10:]) + "</pre>"  # last 10 errors

    if ssh_info is None:
        return f"""
        <h1>Waiting for Ngrok tunnel to start...</h1>
        {error_section}
        """

    try:
        host, port = ssh_info.split(":")
    except ValueError:
        host, port = ssh_info, "?"
        log_error(f"Unexpected format of ngrok ssh info: {ssh_info}")

    return f"""
    <h1>SSH Tunnel Info</h1>
    <p><strong>Username:</strong> appuser</p>
    <p><strong>Password:</strong> choreo123</p>
    <p><strong>Ngrok TCP:</strong> {ssh_info}</p>
    <p><strong>SSH Command:</strong></p>
    <pre>ssh -p {port} appuser@{host}</pre>
    {error_section}
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
