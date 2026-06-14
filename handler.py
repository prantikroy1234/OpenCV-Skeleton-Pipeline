import requests
import threading
import queue
import json


API_ENDPOINT = "http://backend-server/api/detections"   
CAMERA_ID = "CAM_01"                                         
API_TIMEOUT = 5                                             


class APIHandler:
    def __init__(self, endpoint=API_ENDPOINT, camera_id=CAMERA_ID):
        self.endpoint = endpoint
        self.camera_id = camera_id
        self._queue = queue.Queue()
        self._worker = threading.Thread(target=self._process_queue, daemon=True)
        self._running = False

    def start(self):
        self._running = True
        self._worker.start()
        print(f"[APIHandler] Worker thread started. Posting to: {self.endpoint}")

    def stop(self):
        self._running = False
        self._queue.put(None)  
        self._worker.join()
        print("[APIHandler] Worker thread stopped.")

    def post_event(self, image_bytes, detections, timestamp_str):
        event = {
            "image_bytes": image_bytes,
            "detections": detections,
            "timestamp": timestamp_str
        }
        self._queue.put(event)

    def _process_queue(self):
        while self._running:
            event = self._queue.get()

            if event is None:  # Sentinel received — shut down
                break

            self._send(event)

    def _send(self, event):
        metadata = {
            "camera_id": self.camera_id,
            "timestamp": event["timestamp"],
            "detections": [
                {
                    "class_label": d["class_label"],
                    "confidence": round(d["confidence"], 4),
                    "bbox": d["bbox"]
                }
                for d in event["detections"]
            ]
        }

        try:
            response = requests.post(
                self.endpoint,
                files={
                    "image": ("detection.jpg", event["image_bytes"], "image/jpeg")
                },
                data={
                    "metadata": json.dumps(metadata)
                },
                timeout=API_TIMEOUT
            )
            print(f"[APIHandler] Event posted — Status: {response.status_code} | "
                  f"Detections: {len(event['detections'])} | Time: {event['timestamp']}")

        except requests.exceptions.ConnectionError:
            print(f"[APIHandler] Connection failed — could not reach {self.endpoint}")
        except requests.exceptions.Timeout:
            print(f"[APIHandler] Request timed out after {API_TIMEOUT}s")
        except Exception as e:
            print(f"[APIHandler] Unexpected error: {e}")
