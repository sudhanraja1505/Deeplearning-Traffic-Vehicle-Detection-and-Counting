import os
import cv2
from ultralytics import YOLO

VEHICLE_CLASSES = {2: "Car", 3: "Motorcycle", 5: "Bus", 7: "Truck"}


def process_video(input_path, output_path, confidence=0.35):
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("The uploaded video could not be opened.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        cap.release()
        raise ValueError("The video has invalid dimensions.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise ValueError("Could not create output video. Try an MP4 input.")

    line_y = int(height * 0.60)
    counted_ids = set()
    counts = {name: 0 for name in VEHICLE_CLASSES.values()}
    frames = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frames += 1
            results = model.track(
                frame, persist=True, classes=list(VEHICLE_CLASSES.keys()),
                conf=confidence, tracker="bytetrack.yaml", verbose=False
            )
            cv2.line(frame, (0, line_y), (width, line_y), (0, 255, 255), 2)
            cv2.putText(frame, "COUNTING LINE", (10, max(25, line_y - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)

            boxes = results[0].boxes
            if boxes is not None and len(boxes) > 0:
                coords = boxes.xyxy.cpu().numpy().astype(int)
                class_ids = boxes.cls.cpu().numpy().astype(int)
                ids = boxes.id
                track_ids = ids.cpu().numpy().astype(int) if ids is not None else [-1] * len(coords)
                for box, class_id, track_id in zip(coords, class_ids, track_ids):
                    if class_id not in VEHICLE_CLASSES:
                        continue
                    x1, y1, x2, y2 = box.tolist()
                    label = VEHICLE_CLASSES[class_id]
                    center_y = (y1 + y2) // 2
                    if track_id >= 0 and center_y >= line_y and track_id not in counted_ids:
                        counted_ids.add(track_id)
                        counts[label] += 1
                    color = (0, 200, 0) if track_id in counted_ids else (255, 120, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    text = f"{label} ID:{track_id}" if track_id >= 0 else label
                    cv2.putText(frame, text, (x1, max(20, y1 - 8)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

            overlay = [
                f"Total counted: {sum(counts.values())}",
                f"Cars: {counts['Car']}  Motorcycles: {counts['Motorcycle']}",
                f"Buses: {counts['Bus']}  Trucks: {counts['Truck']}",
            ]
            for i, text in enumerate(overlay):
                cv2.putText(frame, text, (10, 30 + i * 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            writer.write(frame)
    finally:
        cap.release()
        writer.release()

    if frames == 0:
        raise ValueError("No readable frames were found in the video.")
    return {"total": sum(counts.values()), "counts": counts, "frames": frames}
