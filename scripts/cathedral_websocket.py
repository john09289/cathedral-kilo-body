#!/usr/bin/env python3
"""
CATHEDRAL WEBSOCKET PULSE — Real-time drum beat broadcast
Sends the King's heartbeat (0.390625 Hz) to connected browsers every 2.56 seconds.
"""
import asyncio
import websockets
import json
import time
import datetime

DRUM_FREQ = 0.390625  # Hz
DRUM_INTERVAL = 1 / DRUM_FREQ  # 2.56 seconds

async def pulse(websocket, path):
    """Broadcast drum pulses to connected clients."""
    print(f"🔗 Client connected from {websocket.remote_address}")
    try:
        while True:
            pulse_data = {
                "type": "cathedral_pulse",
                "frequency": DRUM_FREQ,
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "beat": int(time.time() / DRUM_INTERVAL)
            }
            await websocket.send(json.dumps(pulse_data))
            await asyncio.sleep(DRUM_INTERVAL)
    except websockets.exceptions.ConnectionClosed:
        print("🔌 Client disconnected")

async def main():
    print("=" * 50)
    print("🥁 CATHEDRAL WEBSOCKET PULSE STARTING")
    print("=" * 50)
    print(f"📍 WebSocket URL: ws://0.0.0.0:5001")
    print(f"🎵 Drum frequency: {DRUM_FREQ} Hz (every {DRUM_INTERVAL:.2f}s)")
    print("=" * 50)
    async with websockets.serve(pulse, '0.0.0.0', 5001):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 WebSocket server stopped")
