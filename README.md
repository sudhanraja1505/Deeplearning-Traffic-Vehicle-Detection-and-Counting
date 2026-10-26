# Traffic Vehicle Detection and Counting

A Python deep-learning project that detects cars, motorcycles, buses, and trucks in a traffic video using YOLOv8. It tracks vehicles and counts each tracked vehicle once when it reaches/passes a horizontal counting line. A Flask website lets users upload a video and view/download the processed result.

## Features
- Detects cars, motorcycles, buses, and trucks.
- Tracks vehicles between frames using ByteTrack.
- Counts each tracked vehicle once at the counting line.
- Shows counts by vehicle category and total count.
- Displays bounding boxes and IDs on the processed video.
- Browser-based upload and results page.

## Technologies
Python, YOLOv8 (Ultralytics), OpenCV, Flask, HTML, CSS, ByteTrack.

## Project Structure
```text
Traffic Vehicle Detection and Counting/
├── app.py
├── detector.py
├── requirements.txt
├── README.md
├── templates/index.html
├── static/style.css
├── uploads/
└── outputs/
```
The `uploads` and `outputs` folders are created automatically. YOLOv8 model weights (`yolov8n.pt`) download automatically on the first run if not cached.

## Requirements
- Python 3.10 or 3.11 recommended
- Internet connection for package/model downloads
- A traffic video (`.mp4`, `.avi`, `.mov`, or `.mkv`)

## Installation on Windows / VS Code

Open this folder in VS Code and open Terminal.

### 1. Create a virtual environment
```powershell
py -3.11 -m venv .venv
```

### 2. Activate it
```powershell
.\.venv\Scripts\activate
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\activate
```

### 3. Install dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the application
```powershell
python app.py
```

### 5. Open in your browser
Go to `http://127.0.0.1:5000`, upload a short traffic video, and click **Detect and Count Vehicles**. The first run can take longer while the model downloads.
<img width="1721" height="847" alt="Screenshot 2026-10-26 200209" src="https://github.com/user-attachments/assets/fc94e4ef-5bc5-446a-b7dd-24f4ef635722" />



## How It Works
1. Upload a traffic video.
2. OpenCV reads frames from the video.
3. YOLOv8 detects vehicles in each frame.
4. ByteTrack assigns tracking IDs.
5. A tracked vehicle is counted once when its center reaches/passes the horizontal counting line.
6. The app overlays boxes, labels, IDs, and totals.
7. The processed video and counts are shown on the webpage.

## Limitations
- This is an educational/demo project, not a certified traffic measurement system.
- Current counting logic is best suited to a fixed camera where vehicles move in the expected direction across the line.
- Occlusion, low resolution, camera movement, or lost tracking IDs can affect accuracy.
- The app processes videos locally and may take time for longer videos.

## Troubleshooting

**`ModuleNotFoundError: No module named 'flask'`**
Activate `.venv` and run `python -m pip install -r requirements.txt`.

**`ModuleNotFoundError: No module named 'cv2'`**
Run `python -m pip install opencv-python`.

**YOLO model download fails**
Check your internet connection and start the app again.

**Output video does not play**
Try a common MP4 video. Codec support varies by system.

## Future Enhancements
- Direction-aware line crossing.
- Vehicle speed estimation.
- Traffic density and lane-wise counting.
- Save traffic statistics to a database.
- Deploy to a cloud platform.

## Conclusion
This project demonstrates traffic vehicle detection and counting using object detection and multi-object tracking. It combines YOLOv8, OpenCV, and Flask in a simple browser-based application.
