"""
本地版全雙工 POC — 0 成本
依賴：
  pip install pyaudio requests edge-tts aliyun-python-sdk-core websockets
  ollama serve  # 確保 Ollama 服務在跑
  Ollama 內已 pull：qwen2.5:3b 或 llama3.2:3b
"""

import asyncio
import json
import os
import sys
import time

import edge_tts
import pyaudio
import requests

# 音訊設定
RATE = 16000
CHUNK = 3200  # 200ms
FORMAT = pyaudio.paInt16
CHANNELS = 1

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"  # 或 llama3.2:3b

# 阿里雲 ASR 設定（需自己申請）
ALIYUN_AK_ID = os.environ.get("ALIYUN_AK_ID")
ALIYUN_AK_SECRET = os.environ.get("ALIYUN_AK_SECRET")
ALIYUN_APPKEY = os.environ.get("ALIYUN_APPKEY")

SYSTEM_PROMPT = """你是智家 AI 家具銷售助手。
- 角色：親切、專業、像真人家具顧問
- 語言：繁體中文
- 風格：簡潔，每次 1-2 句話
"""


def asr_transcribe(audio_data: bytes) -> str:
    """
    阿里雲一句話識別（短音訊，< 60s）
    實際生產建議用串流版，這裡為了 POC 用一句話版
    """
    # ⚠️ 這裡只展示架構，實際要申請阿里雲 NLS 服務
    # https://help.aliyun.com/zh/isi/getting-started/start-using-nls-with-the-sdk-for-python

    if not (ALIYUN_AK_ID and ALIYUN_AK_SECRET and ALIYUN_APPKEY):
        print("⚠️ 未設定阿里雲 ASR credentials，使用簡化版：直接丟給 Ollama 用 '我' 觸發回應")
        return "用戶剛說完一段話（請實際整合阿里雲 NLS SDK）"

    # 實際代碼需要 Token + 音訊 base64 + 簽名
    # 參考：https://github.com/aliyun/alibabacloud-nls-python-sdk
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.request import CommonRequest
    import base64

    client = AcsClient(ALIYUN_AK_ID, ALIYUN_AK_SECRET, "cn-shanghai")
    request = CommonRequest()
    request.set_domain("nls-meta.cn-shanghai.aliyuncs.com")
    request.set_version("2019-02-28")
    request.set_action_name("CreateToken")
    token_resp = client.do_action_with_exception(request)
    token = json.loads(token_resp)["Token"]["Id"]

    # 一句話識別
    req = CommonRequest()
    req.set_domain("nls-gateway-cn-shanghai.aliyuncs.com")
    req.set_version("2019-02-28")
    req.set_action_name("RecognizeText")
    req.add_query_param("appkey", ALIYUN_APPKEY)
    req.add_query_param("token", token)
    req.add_query_param("text", base64.b64encode(audio_data).decode())
    req.add_query_param("format", "pcm")
    req.add_query_param("sample_rate", "16000")

    resp = client.do_action_with_exception(req)
    return json.loads(resp).get("Result", "")


async def llm_generate(text: str) -> str:
    """呼叫本地 Ollama LLM 生成回應"""
    prompt = f"{SYSTEM_PROMPT}\n\n用戶說：{text}\n\n助手："

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        return resp.json().get("response", "").strip()
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return "抱歉，我現在有點忙，稍後再聊。"


async def tts_speak(text: str) -> bytes:
    """edge-tts 合成語音，返回 MP3 bytes"""
    communicate = edge_tts.Communicate(text, voice="zh-TW-HsiaoChenNeural")
    mp3_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_data += chunk["data"]
    return mp3_data


def play_audio(mp3_data: bytes):
    """播放 MP3 音訊（簡化版，實際用 ffplay 或 pygame）"""
    import subprocess
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        f.write(mp3_data)
        tmp_path = f.name
    subprocess.run(["ffplay", "-nodisp", "-autoexit", tmp_path],
                   capture_output=True)
    os.unlink(tmp_path)


def record_audio(seconds: int = 5) -> bytes:
    """錄音 N 秒"""
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE,
        input=True, frames_per_buffer=CHUNK
    )

    print(f"🎤 錄音 {seconds} 秒...")
    frames = []
    for _ in range(int(RATE / CHUNK * seconds)):
        frames.append(stream.read(CHUNK))
    print("✅ 錄音完成")

    stream.stop_stream()
    audio.terminate()

    return b"".join(frames)


async def local_voice_loop():
    """本地版對話主迴圈（半雙工，按 Enter 對話）"""
    print("=== AI 家具銷售 POC（本地版）===")
    print("按 Enter 開始錄音 5 秒，AI 會回應")
    print("輸入 'q' 結束\n")

    while True:
        user_input = input("[Enter 開始] > ").strip()
        if user_input.lower() in ("q", "quit", "exit"):
            break

        # 1. 錄音
        audio_data = record_audio(seconds=5)

        # 2. ASR
        user_text = asr_transcribe(audio_data)
        print(f"👤 你: {user_text}")

        if not user_text:
            print("（沒聽清楚，再試一次）")
            continue

        # 3. LLM
        start = time.time()
        ai_text = await llm_generate(user_text)
        llm_time = time.time() - start
        print(f"🤖 AI ({llm_time:.1f}s): {ai_text}")

        # 4. TTS
        mp3_data = await tts_speak(ai_text)
        print(f"🔊 播放 ({len(mp3_data)} bytes)...")
        play_audio(mp3_data)


if __name__ == "__main__":
    print("本地版 POC")
    print("前置：")
    print("  1. ollama serve")
    print(f"  2. ollama pull {OLLAMA_MODEL}")
    print("  3. 設定 ALIYUN_AK_ID / ALIYUN_AK_SECRET / ALIYUN_APPKEY（選用）")
    print("  4. pip install pyaudio requests edge-tts")
    print()
    try:
        asyncio.run(local_voice_loop())
    except KeyboardInterrupt:
        print("\n結束")