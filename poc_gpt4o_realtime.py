"""
GPT-4o Realtime 全雙工 POC
依賴：
  pip install websockets pyaudio
  export OPENAI_API_KEY="sk-..."
"""

import asyncio
import base64
import json
import os
import sys

import pyaudio
import websockets

# 音訊設定
RATE = 24000           # GPT-4o Realtime 預設 24kHz
CHUNK = 4800           # 200ms chunks
FORMAT = pyaudio.paInt16
CHANNELS = 1

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    sys.exit("請先設定環境變數：export OPENAI_API_KEY=sk-...")

URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"

SYSTEM_PROMPT = """你是智家 AI 家具銷售助手。
- 角色：親切、專業、像真人家具顧問
- 能力：推薦家具、解答搭配問題、協助下單
- 語言：繁體中文
- 風格：簡潔有溫度，每次 1-2 句話
"""


async def realtime_voice_chat():
    """GPT-4o Realtime 全雙工對話主程式"""
    async with websockets.connect(
        URL,
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    ) as ws:
        # 1. 設定 session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "instructions": SYSTEM_PROMPT,
                "voice": "alloy",  # 或 'shimmer' / 'echo'
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "turn_detection": {
                    "type": "server_vad",  # 服務器 VAD 自動偵測說話結束
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 200
                }
            }
        }))

        # 2. 音訊串流：麥克風 → WS；WS → 喇叭
        audio = pyaudio.PyAudio()
        mic = audio.open(
            format=FORMAT, channels=CHANNELS, rate=RATE,
            input=True, frames_per_buffer=CHUNK
        )
        speaker = audio.open(
            format=FORMAT, channels=CHANNELS, rate=RATE,
            output=True, frames_per_buffer=CHUNK
        )

        async def send_mic():
            """持續送麥克風音訊到 GPT-4o"""
            print("🎤 開始錄音（按 Ctrl+C 結束）...")
            while True:
                data = mic.read(CHUNK, exception_on_overflow=False)
                await ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": base64.b64encode(data).decode()
                }))
                await asyncio.sleep(0.01)

        async def recv_audio():
            """接收 GPT-4o 回應音訊並播放"""
            async for msg in ws:
                event = json.loads(msg)
                event_type = event.get("type")

                if event_type == "response.audio.delta":
                    audio_data = base64.b64decode(event["delta"])
                    speaker.write(audio_data)

                elif event_type == "response.audio_transcript.delta":
                    text = event.get("delta", "")
                    if text:
                        print(f"🤖 AI: {text}", end="", flush=True)

                elif event_type == "response.audio_transcript.done":
                    print()  # 換行

                elif event_type == "conversation.item.input_audio_transcription.completed":
                    print(f"👤 你: {event.get('transcript', '')}")

                elif event_type == "error":
                    print(f"❌ Error: {event.get('error', {})}")

        try:
            await asyncio.gather(send_mic(), recv_audio())
        finally:
            mic.stop_stream()
            speaker.stop_stream()
            audio.terminate()


if __name__ == "__main__":
    try:
        asyncio.run(realtime_voice_chat())
    except KeyboardInterrupt:
        print("\n結束對話")