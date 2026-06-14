MODEL_PATH = "path/to/your/yolov8_model.pt"    
CONFIDENCE_THRESHOLD = 0.6                     
CLASS_LABELS = []                            



class ObjectDetector:
    def __init__(self, model_path=MODEL_PATH, confidence=CONFIDENCE_THRESHOLD):
        self.model_path = model_path
        self.confidence = confidence
        self.model = None

    def load_model(self):
        print(f"[ObjectDetector] Model ready to load from: {self.model_path}")
        print("[ObjectDetector] Uncomment YOLO lines once ultralytics is installed.")

    def detect(self, frame):
        if self.model is None:
            print("[ObjectDetector] Running in STUB mode — plug in real model to activate.")
            return [
                {
                    "class_label": "object_placeholder",
                    "confidence": 0.91,
                    "bbox": {"x1": 100, "y1": 80, "x2": 300, "y2": 250}
                }
            ]

        # ── REAL INFERENCE (to be uncommented once the model is loaded) ───────────────────
        # results = self.model(frame, conf=self.confidence)[0]
        # detections = []
        # for box in results.boxes:
        #     cls_id = int(box.cls[0])
        #     detections.append({
        #         "class_label": CLASS_LABELS[cls_id] if CLASS_LABELS else str(cls_id),
        #         "confidence": float(box.conf[0]),
        #         "bbox": {
        #             "x1": int(box.xyxy[0][0]),
        #             "y1": int(box.xyxy[0][1]),
        #             "x2": int(box.xyxy[0][2]),
        #             "y2": int(box.xyxy[0][3])
        #         }
        #     })
        # return detections
