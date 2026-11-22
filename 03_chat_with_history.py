"""สัปดาห์ 1 - ตัวอย่างที่ 3: แชทวนลูป โดยจำประวัติการคุย

ประเด็นสำคัญของการเรียนรู้: LLM ไม่มีความจำเอง
ถ้าอยากให้มัน "จำ" ได้ เราต้องส่งประวัติแชททั้งหมดกลับไปทุกครั้ง
(messages list นี้แหละที่จะกลายเป็นหัวใจของ RAG ในสัปดาห์ถัดไป)

ติดตั้งก่อนรัน: pip install -r requirements.txt
รัน: python 03_chat_with_history.py  (พิมพ์ exit เพื่อออก)
"""

import ollama

MODEL_NAME = "qwen2.5:3b"

# เก็บประวัติบทสนทนาไว้ใน list — ทุกครั้งที่คุยต่อ ต้องส่ง list นี้กลับเข้าไปใหม่
chat_history = [
    {"role": "system", "content": "คุณเป็นผู้ช่วยโปรแกรมเมอร์ ตอบกระชับ"},
]

print("พิมพ์คำถามแล้ว Enter (พิมพ์ exit เพื่อออก)\n")

while True:
    user_input = input("คุณ: ").strip()
    if user_input.lower() == "exit":
        break
    if not user_input:
        continue

    chat_history.append({"role": "user", "content": user_input})

    response = ollama.chat(model=MODEL_NAME, messages=chat_history)
    assistant_reply = response["message"]["content"]

    # เก็บคำตอบของโมเดลเข้าประวัติด้วย ไม่งั้นรอบหน้ามันจะจำไม่ได้ว่าตอบอะไรไป
    chat_history.append({"role": "assistant", "content": assistant_reply})

    print(f"โมเดล: {assistant_reply}\n")
