import cv2
import sys
import os


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stream.ingest import StreamIngestor
from inference.detector import ObjectDetector
from annotator.annotate import Annotator
from api.handler import APIHandler



DISPLAY_OUTPUT = True      
SAVE_FRAMES = False        
SAVE_DIR = "output_frames"


def run_pipeline():

    print("=" * 60)
    print("  DeepStream-Architecture CV Pipeline")
    print("  Prototype — Plug in RTSP + YOLOv8 to activate")
    print("=" * 60)

   
    ingestor = StreamIngestor() 
    detector = ObjectDetector()          
    annotator = Annotator()              
    api_handler = APIHandler()           

    if SAVE_FRAMES:
        os.makedirs(SAVE_DIR, exist_ok=True)

    
    try:
        ingestor.connect()
        detector.load_model()
        api_handler.start()
    except ConnectionError as e:
        print(f"[Pipeline] Failed to start: {e}")
        return

    print("\n[Pipeline] Running. Press Q to quit.\n")
    frame_number = 0

    
    while True:

        
        frame, timestamp_ms = ingestor.read_frame()
        if frame is None:
            print("[Pipeline] Stream ended.")
            break

        frame_number += 1
        detections = detector.detect(frame)

       
        if not detections:
            continue

        
        annotated_frame, timestamp_str = annotator.annotate(frame, detections, timestamp_ms)

        
        image_bytes = annotator.encode_frame(annotated_frame)
        api_handler.post_event(image_bytes, detections, timestamp_str)

        
        if DISPLAY_OUTPUT:
            cv2.imshow("DeepStream CV Pipeline — Prototype", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("[Pipeline] User quit.")
                break

        
        if SAVE_FRAMES:
            filename = f"{SAVE_DIR}/frame_{frame_number:06d}.jpg"
            cv2.imwrite(filename, annotated_frame)

    
    ingestor.release()
    api_handler.stop()
    cv2.destroyAllWindows()
    print("[Pipeline] Shutdown complete.")


if __name__ == "__main__":
    run_pipeline()
