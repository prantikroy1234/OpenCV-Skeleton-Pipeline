import cv2
SOURCE = "rtsp://<your_camera_ip>/stream"   
FRAME_SKIP_INTERVAL = 5                     

class StreamIngestor:
 
    def __init__(self, source=SOURCE, interval=FRAME_SKIP_INTERVAL):
        self.source = source
        self.interval = interval
        self.cap = None
        self.frame_count = 0

    def connect(self):
       
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise ConnectionError(f"[StreamIngestor] Could not open source: {self.source}")
        print(f"[StreamIngestor] Connected to source: {self.source}")

    def read_frame(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("[StreamIngestor] Stream ended or connection lost.")
                return None, None

            self.frame_count += 1

            if self.frame_count % self.interval != 0:
                continue

            timestamp_ms = self.cap.get(cv2.CAP_PROP_POS_MSEC)
            return frame, timestamp_ms

    def release(self):
        if self.cap:
            self.cap.release()
            print("[StreamIngestor] Stream released.")
