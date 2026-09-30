#!/usr/bin/env python3
"""
Portable Visual Timer
=====================
A simple visual countdown timer served via HTTP.
Works from a USB key - just run this file and open a browser.

Usage:
    python timer.py [PORT]

Default port: 8080
Open: http://localhost:8080
"""

import http.server
import socketserver
import os
import sys
import threading
from pathlib import Path

PORT = 8080
TOOLBOX_ROOT = Path(__file__).parent.parent

class TimerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve the timer HTML and assets."""

    def do_GET(self):
        if self.path == '/' or self.path == '/timer' or self.path == '/index.html':
            self.serve_toolbox_index()
        elif self.path == '/timer/' or self.path == '/timer/index.html' or self.path == '/timer':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = self.generate_timer_html()
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/timer/..' or self.path == '/timer/../':
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            super().do_GET()

    def serve_toolbox_index(self):
        """Serve the toolbox main index.html"""
        index_path = TOOLBOX_ROOT / 'index.html'
        if index_path.exists():
            with open(index_path, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = self.generate_timer_html()
            self.wfile.write(html.encode('utf-8'))

    def generate_timer_html(self):
        """Generate the complete timer HTML with embedded CSS and JS."""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portable Timer - Toolbox</title>
    <base href="/">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #fff;
            padding: 20px;
        }

        .timer-container {
            text-align: center;
            max-width: 500px;
            width: 100%;
        }

        .timer-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            margin-bottom: 30px;
        }

        .back-link {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(0, 212, 255, 0.3);
            color: #00d4ff;
            padding: 10px 20px;
            border-radius: 10px;
            text-decoration: none;
            font-size: 1rem;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .back-link:hover {
            background: rgba(0, 212, 255, 0.2);
            border-color: #00d4ff;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 30px;
            font-weight: 300;
            color: #00d4ff;
        }

        .timer-display {
            position: relative;
            width: 300px;
            height: 300px;
            margin: 0 auto 40px;
        }

        .timer-circle {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: conic-gradient(#00d4ff 0deg, #333 0deg);
            mask: radial-gradient(circle, transparent 145px, black 150px);
            -webkit-mask: radial-gradient(circle, transparent 145px, black 150px);
            transition: background 0.1s linear;
        }

        .timer-circle-bg {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: #222;
            border: 4px solid #444;
        }

        .timer-center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 3.5rem;
            font-weight: 600;
            color: #00d4ff;
            text-shadow: 0 2px 10px rgba(0, 212, 255, 0.3);
        }

        .time-inputs {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-bottom: 25px;
        }

        .time-input-group {
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .time-input-group label {
            font-size: 0.8rem;
            color: #888;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .time-input {
            width: 80px;
            padding: 12px;
            font-size: 1.5rem;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid #444;
            border-radius: 8px;
            color: #fff;
            text-align: center;
            outline: none;
            transition: border-color 0.3s, background 0.3s;
        }

        .time-input:focus {
            border-color: #00d4ff;
            background: rgba(255, 255, 255, 0.1);
        }

        .buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 15px 30px;
            font-size: 1rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn-start {
            background: linear-gradient(135deg, #00d4ff, #0099cc);
            color: #000;
        }

        .btn-pause {
            background: linear-gradient(135deg, #ff6b6b, #ee5a52);
            color: #fff;
        }

        .btn-reset {
            background: linear-gradient(135deg, #666, #444);
            color: #fff;
        }

        .btn-set {
            background: linear-gradient(135deg, #51cf66, #339af0);
            color: #fff;
        }

        .btn-fullscreen {
            background: linear-gradient(135deg, #a463f2, #8844ee);
            color: #fff;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .status {
            margin-top: 25px;
            font-size: 1.2rem;
            color: #00d4ff;
            min-height: 24px;
        }

        .fullscreen-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            z-index: 1000;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .fullscreen-overlay.active {
            display: flex;
        }

        .fullscreen-timer {
            position: relative;
            width: 80%;
            max-width: 600px;
        }

        .fullscreen-circle {
            position: absolute;
            width: 100%;
            height: 100%;
            padding-top: 100%;
            border-radius: 50%;
            background: conic-gradient(#00d4ff 0deg, #333 0deg);
            mask: radial-gradient(circle, transparent 145px, black 150px);
            -webkit-mask: radial-gradient(circle, transparent calc(100% - 4px), black 100%);
        }

        .fullscreen-circle-bg {
            position: absolute;
            width: 100%;
            height: 100%;
            padding-top: 100%;
            border-radius: 50%;
            background: #222;
        }

        .fullscreen-center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 10vw;
            font-weight: 600;
            color: #00d4ff;
            text-shadow: 0 4px 20px rgba(0, 212, 255, 0.5);
        }

        .fullscreen-exit {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            color: #fff;
            font-size: 2rem;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .fullscreen-exit:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        .keyboard-hint {
            margin-top: 30px;
            font-size: 0.8rem;
            color: #555;
            text-align: center;
            max-width: 400px;
        }

        .keyboard-hint span {
            color: #00d4ff;
            margin: 0 3px;
        }

        @media (max-width: 600px) {
            h1 {
                font-size: 1.8rem;
            }

            .timer-display {
                width: 250px;
                height: 250px;
            }

            .timer-center {
                font-size: 2.5rem;
            }

            .time-input {
                width: 60px;
                padding: 10px;
                font-size: 1.2rem;
            }
        }
    </style>
</head>
<body>
    <div class="timer-container">
        <div class="timer-header">
            <a href="/" class="back-link">← Toolbox</a>
        </div>

        <h1>Portable Timer</h1>

        <div class="timer-display">
            <div class="timer-circle-bg"></div>
            <div class="timer-circle" id="timerCircle"></div>
            <div class="timer-center" id="timerDisplay">00:00:00</div>
        </div>

        <div class="time-inputs">
            <div class="time-input-group">
                <label>Hours</label>
                <input type="number" class="time-input" id="hoursInput" min="0" max="23" value="0">
            </div>
            <div class="time-input-group">
                <label>Minutes</label>
                <input type="number" class="time-input" id="minutesInput" min="0" max="59" value="1">
            </div>
            <div class="time-input-group">
                <label>Seconds</label>
                <input type="number" class="time-input" id="secondsInput" min="0" max="59" value="0">
            </div>
        </div>

        <div class="buttons">
            <button class="btn btn-set" id="setBtn">Set Time</button>
            <button class="btn btn-start" id="startBtn">Start</button>
            <button class="btn btn-pause" id="pauseBtn" disabled>Pause</button>
            <button class="btn btn-reset" id="resetBtn">Reset</button>
            <button class="btn btn-fullscreen" id="fullscreenBtn">Fullscreen</button>
        </div>

        <div class="status" id="status"></div>

        <div class="keyboard-hint">
            <span>Space</span> to start/pause | <span>R</span> to reset | <span>Esc</span> to exit fullscreen | <span>←</span> to return to toolbox
        </div>
    </div>

    <div class="fullscreen-overlay" id="fullscreenOverlay">
        <button class="fullscreen-exit" id="fullscreenExit">&times;</button>
        <div class="fullscreen-timer">
            <div class="fullscreen-circle-bg"></div>
            <div class="fullscreen-circle" id="fullscreenCircle"></div>
            <div class="fullscreen-center" id="fullscreenDisplay">00:00:00</div>
        </div>
    </div>

    <script>
        let totalSeconds = 0;
        let remainingSeconds = 0;
        let timerInterval = null;
        let isRunning = false;
        let endTime = null;

        const timerDisplay = document.getElementById('timerDisplay');
        const fullscreenDisplay = document.getElementById('fullscreenDisplay');
        const timerCircle = document.getElementById('timerCircle');
        const fullscreenCircle = document.getElementById('fullscreenCircle');
        const hoursInput = document.getElementById('hoursInput');
        const minutesInput = document.getElementById('minutesInput');
        const secondsInput = document.getElementById('secondsInput');
        const setBtn = document.getElementById('setBtn');
        const startBtn = document.getElementById('startBtn');
        const pauseBtn = document.getElementById('pauseBtn');
        const resetBtn = document.getElementById('resetBtn');
        const fullscreenBtn = document.getElementById('fullscreenBtn');
        const fullscreenOverlay = document.getElementById('fullscreenOverlay');
        const fullscreenExit = document.getElementById('fullscreenExit');
        const status = document.getElementById('status');

        function formatTime(seconds) {
            const h = Math.floor(seconds / 3600);
            const m = Math.floor((seconds % 3600) / 60);
            const s = seconds % 60;
            return h.toString().padStart(2, '0') + ':' + m.toString().padStart(2, '0') + ':' + s.toString().padStart(2, '0');
        }

        function updateDisplay() {
            const display = formatTime(remainingSeconds);
            timerDisplay.textContent = display;
            fullscreenDisplay.textContent = display;
            const progress = totalSeconds > 0 ? ((totalSeconds - remainingSeconds) / totalSeconds) * 360 : 0;
            timerCircle.style.background = 'conic-gradient(#00d4ff ' + progress + 'deg, #333 0deg)';
            fullscreenCircle.style.background = 'conic-gradient(#00d4ff ' + progress + 'deg, #333 0deg)';
        }

        function setTime() {
            const hours = parseInt(hoursInput.value) || 0;
            const minutes = parseInt(minutesInput.value) || 0;
            const seconds = parseInt(secondsInput.value) || 0;
            totalSeconds = hours * 3600 + minutes * 60 + seconds;
            remainingSeconds = totalSeconds;
            updateDisplay();
            status.textContent = 'Time set: ' + formatTime(totalSeconds);
            startBtn.disabled = totalSeconds === 0;
        }

        function startTimer() {
            if (isRunning || totalSeconds === 0) return;
            isRunning = true;
            startBtn.disabled = true;
            pauseBtn.disabled = false;
            setBtn.disabled = true;
            endTime = Date.now() + remainingSeconds * 1000;
            timerInterval = setInterval(function() {
                remainingSeconds = Math.max(0, Math.ceil((endTime - Date.now()) / 1000));
                updateDisplay();
                if (remainingSeconds <= 0) {
                    clearInterval(timerInterval);
                    isRunning = false;
                    startBtn.disabled = false;
                    pauseBtn.disabled = true;
                    setBtn.disabled = false;
                    playNotification();
                    status.textContent = \"Time's up!\";
                    const originalColor = timerDisplay.style.color;
                    let flashCount = 0;
                    const flashInterval = setInterval(function() {
                        timerDisplay.style.color = flashCount % 2 === 0 ? '#ff4444' : '#00d4ff';
                        fullscreenDisplay.style.color = flashCount % 2 === 0 ? '#ff4444' : '#00d4ff';
                        flashCount++;
                        if (flashCount >= 10) {
                            clearInterval(flashInterval);
                            timerDisplay.style.color = originalColor;
                            fullscreenDisplay.style.color = originalColor;
                        }
                    }, 300);
                }
            }, 50);
            status.textContent = \"Running...\";
        }

        function pauseTimer() {
            if (!isRunning) return;
            isRunning = false;
            startBtn.disabled = false;
            pauseBtn.disabled = true;
            setBtn.disabled = false;
            clearInterval(timerInterval);
            const elapsed = Math.floor((Date.now() - (endTime - remainingSeconds * 1000)) / 1000);
            remainingSeconds = Math.max(0, totalSeconds - elapsed);
            status.textContent = \"Paused\";
        }

        function resetTimer() {
            clearInterval(timerInterval);
            isRunning = false;
            startBtn.disabled = totalSeconds === 0;
            pauseBtn.disabled = true;
            setBtn.disabled = false;
            remainingSeconds = totalSeconds;
            updateDisplay();
            status.textContent = 'Reset to ' + formatTime(totalSeconds);
        }

        function toggleFullscreen() {
            if (fullscreenOverlay.classList.contains('active')) {
                exitFullscreen();
            } else {
                enterFullscreen();
            }
        }

        function enterFullscreen() {
            fullscreenOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
            fullscreenBtn.textContent = 'Exit Fullscreen';
            const elem = document.documentElement;
            if (elem.requestFullscreen) {
                elem.requestFullscreen().catch(function(err) {
                    console.log('Fullscreen error:', err);
                });
            }
        }

        function exitFullscreen() {
            fullscreenOverlay.classList.remove('active');
            document.body.style.overflow = '';
            fullscreenBtn.textContent = 'Fullscreen';
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }

        function playNotification() {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            oscillator.frequency.value = 800;
            oscillator.type = 'sine';
            gainNode.gain.value = 0.1;
            oscillator.start();
            let time = audioContext.currentTime;
            gainNode.gain.setValueAtTime(0.1, time);
            gainNode.gain.exponentialRampToValueAtTime(0.001, time + 0.2);
            oscillator.frequency.setValueAtTime(1000, time + 0.25);
            gainNode.gain.setValueAtTime(0.1, time + 0.25);
            gainNode.gain.exponentialRampToValueAtTime(0.001, time + 0.45);
            oscillator.frequency.setValueAtTime(1200, time + 0.5);
            gainNode.gain.setValueAtTime(0.1, time + 0.5);
            gainNode.gain.exponentialRampToValueAtTime(0.001, time + 0.7);
            oscillator.stop(time + 0.8);
        }

        setBtn.addEventListener('click', setTime);
        startBtn.addEventListener('click', startTimer);
        pauseBtn.addEventListener('click', pauseTimer);
        resetBtn.addEventListener('click', resetTimer);
        fullscreenBtn.addEventListener('click', toggleFullscreen);
        fullscreenExit.addEventListener('click', exitFullscreen);

        document.addEventListener('keydown', function(e) {
            if (e.target.tagName === 'INPUT') {
                if (e.key === 'Enter') {
                    setTime();
                    startTimer();
                }
                return;
            }
            switch (e.code) {
                case 'Space':
                    e.preventDefault();
                    if (isRunning) {
                        pauseTimer();
                    } else if (totalSeconds > 0) {
                        startTimer();
                    }
                    break;
                case 'KeyR':
                    resetTimer();
                    break;
                case 'Escape':
                    if (fullscreenOverlay.classList.contains('active')) {
                        exitFullscreen();
                    }
                    break;
            }
        });

        updateDisplay();
        startBtn.disabled = totalSeconds === 0;

        document.addEventListener('fullscreenchange', function() {
            if (!document.fullscreenElement) {
                exitFullscreen();
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.code === 'Space' && e.target === document.body) {
                e.preventDefault();
            }
            if (e.code === 'Backspace' || e.code === 'ArrowLeft') {
                e.preventDefault();
                window.location.href = '/';
            }
        });
    </script>
</body>
</html>'''

def run_server(port):
    """Start the HTTP server."""
    handler = TimerHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\\n{'='*50}")
        print(f"  Portable Visual Timer")
        print(f"{'='*50}")
        print(f"\\n  Server running at: http://localhost:{port}")
        print(f"  Press Ctrl+C to stop")
        print(f"\\n  Controls:")
        print(f"    - Set time and click 'Set Time'")
        print(f"    - Space: Start/Pause")
        print(f"    - R: Reset")
        print(f"    - F: Fullscreen (or click Fullscreen button)")
        print(f"    - Esc: Exit fullscreen")
        print(f"    - <-: Return to toolbox")
        print(f"\\n{'='*50}\\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\n\\nServer stopped.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}. Using default port {PORT}.")
    run_server(PORT)