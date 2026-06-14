import cv2
import datetime


class Annotator:
    BOX_COLOR = (0, 255, 0)        # Green bounding boxes
    TEXT_COLOR = (255, 255, 255)   # White text
    BOX_THICKNESS = 2
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.6
    FONT_THICKNESS = 2

    def annotate(self, frame, detections, timestamp_ms=None):
        annotated = frame.copy()
        for det in detections:
            bbox = det["bbox"]
            label = f"{det['class_label']} {det['confidence']:.2f}"
            cv2.rectangle(
                annotated,
                (bbox["x1"], bbox["y1"]),
                (bbox["x2"], bbox["y2"]),
                self.BOX_COLOR,
                self.BOX_THICKNESS
            )
            (text_w, text_h), _ = cv2.getTextSize(
                label, self.FONT, self.FONT_SCALE, self.FONT_THICKNESS
            )
            cv2.rectangle(
                annotated,
                (bbox["x1"], bbox["y1"] - text_h - 8),
                (bbox["x1"] + text_w + 4, bbox["y1"]),
                self.BOX_COLOR,
                -1  
            )
            cv2.putText(
                annotated,
                label,
                (bbox["x1"] + 2, bbox["y1"] - 4),
                self.FONT,
                self.FONT_SCALE,
                self.TEXT_COLOR,
                self.FONT_THICKNESS
            )
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        cv2.putText(
            annotated,
            timestamp_str,
            (10, 30),
            self.FONT,
            0.7,
            (0, 255, 255),  # Yellow timestamp
            2
        )

        return annotated, timestamp_str

    def encode_frame(self, frame):
        _, buffer = cv2.imencode(".jpg", frame)
        return buffer.tobytes()
