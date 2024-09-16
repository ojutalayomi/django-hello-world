from django.http import HttpResponse
import requests
import time
import threading
import logging
from datetime import datetime

url = "https://velo-xso2.onrender.com/api/socket"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def keep_alive_task():
    while True:
        try:
            response = requests.get(url)
            logger.info(f"{datetime.now()} - Keep-alive request sent. Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"{datetime.now()} - Error sending keep-alive request: {e}")
        time.sleep(240)  # Send a request every 4 minutes

# Start the keep-alive task in a separate thread
keep_alive_thread = threading.Thread(target=keep_alive_task, daemon=True)
keep_alive_thread.start()


def keep_alive(request):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return HttpResponse("OK", status=200)
        else:
            return HttpResponse("Error", status=500)
    except requests.RequestException as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
