import subprocess
import sys
import os
from threading import Thread
import time

def run_flask():
    os.environ['FLASK_APP'] = 'run.py'
    subprocess.run([sys.executable, "-m", "flask", "run"])

def run_streamlit():
    # Wait a moment for Flask to start
    time.sleep(2)
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "app/streamlit_app.py",
        "--server.port", "8501"
    ])

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run Streamlit in the main thread
    run_streamlit() 