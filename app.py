
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import os
import queue
import threading
import time
from automation_logic import run_automation

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global queue for log streaming
log_queue = queue.Queue()

def logger_callback(message):
    print(message) # Print to console
    log_queue.put(message) # Put in queue for frontend

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_automation():
    uid = request.form.get('uid')
    password = request.form.get('password')
    doctor_name = request.form.get('doctor_name')
    file = request.files.get('file')

    if not uid or not password or not doctor_name or not file:
        return jsonify({'error': 'Missing fields'}), 400

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Clear previous logs
    with log_queue.mutex:
        log_queue.queue.clear()

    # Run automation in a separate thread so it doesn't block the request
    thread = threading.Thread(target=run_automation, args=(filepath, uid, password, doctor_name, logger_callback))
    thread.start()

    return jsonify({'status': 'Automation started', 'message': 'Check logs for progress.'})

@app.route('/stream_logs')
def stream_logs():
    def generate():
        while True:
            try:
                # Wait for log with a timeout
                message = log_queue.get(timeout=1)
                yield f"data: {message}\n\n"
            except queue.Empty:
                # Send a keep-alive comment
                yield ": keep-alive\n\n"
            except Exception as e:
                yield f"data: Error: {e}\n\n"
                break
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
