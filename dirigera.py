import json
import os
import re
import ssl
import subprocess
import time

import websocket


DIRIGERA_IP = "192.168.0.6"
WEBSOCKET_URL = f"wss://{DIRIGERA_IP}:8443/v1"

BADØYE_ID = "6461ef0e-a6c7-4edd-9eb2-07fdf215289a_1"

TOKEN_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "dirigera_token.txt",
)


# ============================================================
# TOKEN MANAGEMENT
# ============================================================

def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None

    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            token = f.read().strip()

        return token or None

    except OSError as e:
        print(f"Could not read token cache: {e}")
        return None


def save_token(token):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token)

    print("Token cached.")


def delete_token():
    try:
        os.remove(TOKEN_FILE)
        print("Cached token deleted.")
    except FileNotFoundError:
        pass


def generate_token():
    print()
    print("==========================================")
    print(" DIRIGERA AUTHENTICATION REQUIRED")
    print("==========================================")
    print()
    print("Press the action button on DIRIGERA.")
    print("Then press ENTER when prompted.")
    print()

    result = subprocess.run(
        ["generate-token", DIRIGERA_IP],
        capture_output=True,
        text=True,
    )

    output = result.stdout + result.stderr

    match = re.search(
        r"Your TOKEN\s*:\s*\r?\n?"
        r"([A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)",
        output,
    )

    if not match:
        print("generate-token output:")
        print(output)
        raise RuntimeError("Could not extract DIRIGERA token.")

    token = match.group(1)

    save_token(token)

    return token


def get_token():
    token = load_token()

    if token:
        print("Using cached DIRIGERA token.")
        return token

    return generate_token()


# ============================================================
# WEBSOCKET
# ============================================================

def on_open(ws):
    print("Connected to DIRIGERA")

    # Initialize the connection
    ws.send("{}")


def on_message(ws, message):
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        print("Non-JSON message:")
        print(message)
        return

    print()
    print("EVENT:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    event_text = json.dumps(data)

    if BADØYE_ID in event_text:
        print()
        print(">>> BADØYE EVENT <<<")


def on_error(ws, error):
    print()
    print("WebSocket error:")
    print(error)


def on_close(ws, status_code, message):
    print()
    print(f"WebSocket closed: {status_code} {message}")


# ============================================================
# CONNECTION
# ============================================================

def create_websocket(token):
    return websocket.WebSocketApp(
        WEBSOCKET_URL,
        header=[
            f"Authorization: Bearer {token}"
        ],
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )


def connect(token):
    """
    Returns:
        True  = connection was established
        False = connection failed
    """

    connected = False
    authentication_failed = False

    def local_on_open(ws):
        nonlocal connected

        connected = True
        print("Connected to DIRIGERA")

        # Subscribe to all device events
        ws.send(json.dumps({
            "action": "subscribe",
            "id": "events"
        }))

    def local_on_error(ws, error):
        nonlocal authentication_failed

        error_text = str(error)

        print()
        print("WebSocket error:")
        print(error_text)

        # websocket-client commonly reports HTTP handshake
        # failures through WebSocketBadStatusException.
        if "401" in error_text or "403" in error_text:
            authentication_failed = True

    def local_on_message(ws, message):
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            print("Non-JSON message:")
            print(message)
            return

        print()
        print("EVENT:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        event_text = json.dumps(data)

        if BADØYE_ID in event_text:
            print()
            print(">>> BADØYE EVENT <<<")

    def local_on_close(ws, status_code, message):
        print()
        print(f"WebSocket closed: {status_code} {message}")

    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        header=[
            f"Authorization: Bearer {token}"
        ],
        on_open=local_on_open,
        on_message=local_on_message,
        on_error=local_on_error,
        on_close=local_on_close,
    )

    try:
        ws.run_forever(
            sslopt={
                "cert_reqs": ssl.CERT_NONE
            }
        )

    except Exception as e:
        error_text = str(e)

        print()
        print(f"Connection exception: {error_text}")

        if "401" in error_text or "403" in error_text:
            authentication_failed = True

    return authentication_failed


# ============================================================
# MAIN LOOP
# ============================================================

def main():

    token = get_token()

    while True:

        print()
        print("------------------------------------------")
        print("Connecting to DIRIGERA...")
        print("------------------------------------------")

        authentication_failed = connect(token)

        if authentication_failed:

            # ------------------------------------------------
            # TOKEN IS INVALID
            # ------------------------------------------------

            print()
            print("DIRIGERA rejected the cached token.")
            print("A new token is required.")

            delete_token()

            # Manual button press happens here.
            token = generate_token()

            print()
            print("New token obtained.")
            print("Retrying connection...")

            continue

        # ----------------------------------------------------
        # NORMAL DISCONNECT
        # ----------------------------------------------------

        print()
        print("Normal connection lost.")
        print("Keeping cached token.")

        print("Reconnecting in 5 seconds...")
        time.sleep(5)


if __name__ == "__main__":
    main()