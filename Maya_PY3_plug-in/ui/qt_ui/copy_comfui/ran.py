# -*- coding: utf-8 -*-
import uvicorn
import webbrowser
import threading
import time
from main import app

def start_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    threading.Thread(target=start_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)