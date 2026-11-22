"""สัปดาห์ 1 - ตัวอย่างที่ 2: เรียก LLM ด้วย package ollama

ตัวอย่างที่ 1 เราเขียน HTTP เองทั้งหมด ตัวอย่างนี้ใช้ package ที่เขาห่อไว้ให้
(เทียบกับ C# คือเหมือนติดตั้ง NuGet package แล้วเรียก client สำเร็จรูป)

ติดตั้งก่อนรัน: pip install -r requirements.txt
รัน: python 02_ollama_package.py
"""

import ollama

MODEL_NAME = "qwen2.5:3b"

response = ollama.chat(
    model=MODEL_NAME,
    messages=[
        # role "system" = กำหนดบุคลิก/กฎให้โมเดล เหมือนการ set context
        {"role": "system", "content": "คุณเป็นผู้ช่วยที่ตอบสั้นกระชับและตรงประเด็น"},
        # role "user" = คำถามของผู้ใช้
        {"role": "user", "content": "REST API ต่างจาก gRPC ยังไง ตอบ 2 ข้อ"},
    ],
)

print(response["message"]["content"])
