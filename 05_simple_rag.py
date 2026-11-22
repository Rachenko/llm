"""สัปดาห์ 2 - ตัวอย่างที่ 5: RAG แบบเห็นทุกขั้นตอน

RAG = Retrieval-Augmented Generation
  1. Retrieval   : ค้นหาชิ้นเอกสารที่เกี่ยวกับคำถาม (ด้วย embedding จากตัวอย่าง 4)
  2. Augmented   : เอาชิ้นเอกสารนั้นแปะเข้าไปใน prompt
  3. Generation  : ให้ LLM ตอบ โดยอ่านจากเอกสารที่แปะให้

รัน: python 05_simple_rag.py
"""

import ollama

from rag_utils import (
    CHAT_MODEL,
    RAG_SYSTEM_PROMPT,
    build_context,
    load_or_build_index,
    search,
)

question = "ทำงานมา 3 ปี ได้ลาพักร้อนกี่วัน แล้วใช้ไม่หมดยกไปปีหน้าได้ไหม"
print(f"คำถาม: {question}\n")

# ---- ลองถามแบบไม่มี RAG ก่อน: โมเดลไม่รู้จักบริษัทเรา จะเดาหรือตอบกว้างๆ ----
print("=== ตอบแบบไม่มี RAG ===")
response_without_rag = ollama.chat(
    model=CHAT_MODEL,
    messages=[{"role": "user", "content": question}],
)
print(response_without_rag["message"]["content"], "\n")

# ---- ขั้นที่ 0: เตรียม index (อ่านเอกสาร + หั่นเป็นชิ้น + แปลงเป็น vector) ----
index = load_or_build_index()

# ---- ขั้นที่ 1 Retrieval: หาชิ้นเอกสารที่ใกล้คำถามที่สุด ----
found_chunks = search(index, question, top_k=3)
print("=== ชิ้นเอกสารที่ค้นเจอ ===")
for chunk in found_chunks:
    first_line_of_section = chunk["text"].splitlines()[1]
    print(f"  {chunk['score']:.3f}  {chunk['source']}  {first_line_of_section}")
print()

# ---- ขั้นที่ 2 Augmented: แปะเอกสารลงใน prompt ----
context = build_context(found_chunks)
user_message = f"เอกสารอ้างอิง:\n{context}\n\nคำถาม: {question}"

# ---- ขั้นที่ 3 Generation: ให้ LLM ตอบจากเอกสาร ----
print("=== ตอบแบบมี RAG ===")
response_with_rag = ollama.chat(
    model=CHAT_MODEL,
    messages=[
        {"role": "system", "content": RAG_SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ],
    options={"temperature": 0},  # 0 = ตอบตรงตามเอกสาร ไม่ใส่ความคิดสร้างสรรค์
)
print(response_with_rag["message"]["content"])
