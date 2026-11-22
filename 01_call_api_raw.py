"""สัปดาห์ 1 - ตัวอย่างที่ 1: เรียก LLM ด้วย HTTP request เปล่าๆ

ไม่ต้องติดตั้ง library อะไรเลย ใช้แค่ standard library ของ Python
เพื่อให้เห็นว่าการเรียก LLM ก็คือการยิง HTTP POST ส่ง JSON ธรรมดา
(เทียบกับ C# คือเหมือน HttpClient.PostAsync แล้วอ่าน JSON กลับ)

รัน: python 01_call_api_raw.py
"""

import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"


def ask_llm(prompt_text: str) -> str:
    request_body = {
        "model": MODEL_NAME,
        "prompt": prompt_text,
        "stream": False,  # รอคำตอบทั้งก้อนเดียว ไม่ทยอยส่ง
    }

    http_request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(request_body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(http_request) as http_response:
        response_body = json.loads(http_response.read().decode("utf-8"))

    return response_body["response"]


if __name__ == "__main__":
    user_question = "อธิบายว่า API คืออะไร สั้นๆ 2 ประโยค สำหรับโปรแกรมเมอร์"
    print("ถาม:", user_question)
    print("ตอบ:", ask_llm(user_question))
