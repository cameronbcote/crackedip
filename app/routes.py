from app import app
from flask import render_template, Response, jsonify
import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_cracks(frame):
    # ... (keep existing code)

def gen_frames():
    try:
        camera = cv2.VideoCapture(0)
        while True:
            success, frame = camera.read()
            if not success:
                logger.error("Failed to capture frame")
                break
            else:
                frame, has_cracks = detect_cracks(frame)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        logger.error(f"Error in gen_frames: {str(e)}")
    finally:
        camera.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}")
    return jsonify(error="Internal Server Error"), 500