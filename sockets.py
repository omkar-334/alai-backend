import json
import os

from websocket import WebSocketApp

from models import Layout


def create_variants(ppt_id, slide_id, instructions, context, images: list = [], layout=Layout.AI_GENERATED):
    received_messages = []

    print("Creating variants...")

    def on_message(ws, message):
        # print("Received message:")
        # print(message)
        received_messages.append(message)

    def on_error(ws, error):
        print("Error:", error)

    def on_close(ws, close_status_code, close_msg):
        print("Connection closed:", close_status_code, close_msg)
        # print("\nAll received messages:")
        # for i, msg in enumerate(received_messages, 1):
        #     print(f"[{i}] {msg}")

    def on_open(ws):
        payload = {
            "presentation_id": ppt_id,
            "slide_id": slide_id,
            "layout_type": layout.value,
            "images_on_slide": images,
            "additional_instructions": instructions,
            "slide_specific_context": context,
            "update_tone_verbosity_calibration_status": True,
            "auth_token": os.getenv("TOKEN"),
        }

        ws.send(json.dumps(payload))
        print("Payload sent.")

    ws = WebSocketApp(
        "wss://alai-standalone-backend.getalai.com/ws/create-and-stream-slide-variants",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()

    return received_messages
