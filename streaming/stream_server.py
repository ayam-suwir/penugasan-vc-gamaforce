import cv2
from flask import Flask, Response, render_template_string
import socket

app = Flask(__name__)

# Konfigurasi untuk latensi rendah
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_RATE = 30
JPEG_QUALITY = 80

# Inisialisasi kamera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
camera.set(cv2.CAP_PROP_FPS, FRAME_RATE)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
        
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Camera Streaming</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                padding: 30px;
                max-width: 800px;
                width: 100%;
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 10px;
                font-size: 28px;
            }}
            .info {{
                text-align: center;
                color: #666;
                margin-bottom: 20px;
                font-size: 14px;
            }}
            .video-container {{
                position: relative;
                width: 100%;
                border-radius: 10px;
                overflow: hidden;
                background: #000;
                box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            }}
            img {{
                width: 100%;
                height: auto;
                display: block;
            }}
            .stats {{
                margin-top: 20px;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
            }}
            .stat-box {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }}
            .stat-label {{
                font-size: 12px;
                color: #666;
                text-transform: uppercase;
                margin-bottom: 5px;
            }}
            .stat-value {{
                font-size: 18px;
                font-weight: bold;
                color: #667eea;
            }}
            .status {{
                display: inline-block;
                padding: 5px 15px;
                background: #28a745;
                color: white;
                border-radius: 20px;
                font-size: 12px;
                margin-top: 10px;
            }}
            @media (max-width: 600px) {{
                .container {{
                    padding: 20px;
                }}
                h1 {{
                    font-size: 22px;
                }}
                .stats {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Camera Streaming</h1>
            <div class="info">
                Live Video Feed
                <div class="status">LIVE</div>
            </div>
            
            <div class="video-container">
                <img src="/video_feed" alt="Video Stream">
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-label">Resolution</div>
                    <div class="stat-value">{FRAME_WIDTH}x{FRAME_HEIGHT}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Frame Rate</div>
                    <div class="stat-value">{FRAME_RATE} FPS</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Quality</div>
                    <div class="stat-value">{JPEG_QUALITY}%</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000
    
    print("=" * 70)
    print("CAMERA STREAMING SERVER")
    print("=" * 70)
    print(f"Server berjalan di: http://{local_ip}:{port}")
    print(f"Resolusi: {FRAME_WIDTH}x{FRAME_HEIGHT}")
    print(f"Frame Rate: {FRAME_RATE} FPS")
    print(f"JPEG Quality: {JPEG_QUALITY}%")
    print("-" * 70)

    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)