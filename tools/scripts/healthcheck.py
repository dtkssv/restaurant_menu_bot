"""HEALTHCHECK Script
Perform HTTP requests against the API /status endpoint, as Docker healthchecks
"""

import os
import sys
import urllib.request
import urllib.error

try:
    from fastapi-project.settings import api_settings
except ModuleNotFoundError:
    sys.path.append(os.getcwd())
    from fastapi-project.settings import api_settings


def healthcheck():
    try:
        with urllib.request.urlopen(f"http://localhost:{api_settings.port}/status") as response:
            code = response.getcode()
            text = response.read().decode()
            print(f"Healthcheck response ({code}): {text}")
    except urllib.error.URLError as ex:
        print(f"Healthcheck failed ({ex})")


if __name__ == "__main__":
    healthcheck()