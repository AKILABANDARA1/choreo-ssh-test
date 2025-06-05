import time
import os

LOG_FILE = "/tmp/ngrok.log"

def tail_log():
    last_size = 0
    while True:
        if os.path.exists(LOG_FILE):
            size = os.path.getsize(LOG_FILE)
            if size > last_size:
                with open(LOG_FILE, "r") as f:
                    f.seek(last_size)
                    new_data = f.read()
                    print(f"New ngrok log data:\n{new_data}")
                    last_size = size
        else:
            print(f"{LOG_FILE} does not exist yet.")
        time.sleep(5)

if __name__ == "__main__":
    try:
        tail_log()
    except KeyboardInterrupt:
        print("Exiting log tailer.")
