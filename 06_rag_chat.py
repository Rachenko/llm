"""สัปดาห์ 2 - ตัวอย่างที่ 6: แชทบอทถาม-ตอบเอกสารบริษัท (RAG + ประวัติแชท)

รวมตัวอย่าง 3 (แชทจำประวัติ) กับตัวอย่าง 5 (RAG) เข้าด้วยกัน
ทุกคำถาม: ค้นเอกสารใหม่ -> แปะเอกสารเข้าไปกับคำถาม -> ส่งพร้อมประวัติแชทให้ LLM ตอบ

ลองเอาเอกสารของคุณเองมาใส่ในโฟลเดอร์ data/ (ไฟล์ .md แบ่งหัวข้อด้วย "## ") แล้วรันใหม่ได้เลย
รัน: python 06_rag_chat.py  (พิมพ์ exit เพื่อออก)
"""

import ollama

from rag_utils import (
    CHAT_MODEL,
    RAG_SYSTEM_PROMPT,
    build_context,
    load_or_build_index,
    search,
)

index = load_or_build_index()

chat_history = [{"role": "system", "content": RAG_SYSTEM_PROMPT}]

print("ถามเรื่องการลา WFH เบิกค่าใช้จ่าย IT หรือสวัสดิการได้เลย (พิมพ์ exit เพื่อออก)")
print("ตัวอย่าง: ลาป่วยกี่วันถึงต้องใช้ใบรับรองแพทย์ / โน้ตบุ๊กหายต้องทำไง\n")

while True:
    question = input("คุณ: ").strip()
    if question.lower() == "exit":
        break
    if not question:
        continue

    found_chunks = search(index, question, top_k=3)
    context = build_context(found_chunks)

    # ส่งเอกสาร + คำถามไปให้โมเดลในรอบนี้
    messages_for_this_turn = chat_history + [
        {"role": "user", "content": f"เอกสารอ้างอิง:\n{context}\n\nคำถาม: {question}"}
    ]
    # temperature 0 = ตอบตรงตามเอกสาร ไม่ใส่ความคิดสร้างสรรค์
    response = ollama.chat(model=CHAT_MODEL, messages=messages_for_this_turn, options={"temperature": 0})
    assistant_reply = response["message"]["content"]

    # ประวัติเก็บแค่คำถามเปล่าๆ ไม่เก็บเอกสาร ไม่งั้น prompt จะยาวขึ้นเรื่อยๆ ทุกรอบ
    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": assistant_reply})

    sources = sorted({chunk["source"] for chunk in found_chunks})
    print(f"โมเดล: {assistant_reply}")
    print(f"(อ้างอิง: {', '.join(sources)})\n")
