"""สัปดาห์ 2 - ตัวอย่างที่ 4: Embedding คืออะไร

Embedding = แปลงข้อความเป็น list ของตัวเลข (vector) ที่เก็บ "ความหมาย" ไว้
ข้อความที่ความหมายใกล้กัน ตัวเลขจะใกล้กัน ถึงจะใช้คำคนละคำก็ตาม
นี่คือวิธีที่ RAG ใช้ "ค้นหา" เอกสารที่เกี่ยวกับคำถาม

ติดตั้งก่อนรัน: ollama pull bge-m3
รัน: python 04_embeddings.py
"""

from rag_utils import cosine_similarity, embed_texts

sentences = [
    "ลาป่วยต้องมีใบรับรองแพทย์ไหม",
    "ไม่สบาย หยุดงาน 3 วัน ต้องใช้เอกสารอะไร",
    "เบิกค่าแท็กซี่ไปหาลูกค้าได้ไหม",
    "วันนี้ฝนตกหนักมาก",
]

vectors = embed_texts(sentences)

print(f"1 ประโยค ถูกแปลงเป็นตัวเลข {len(vectors[0])} ตัว")
print(f"ตัวอย่าง 5 ตัวแรกของประโยคแรก: {[round(number, 4) for number in vectors[0][:5]]}\n")

print(f'เทียบความหมายกับประโยค: "{sentences[0]}"')
for sentence, vector in zip(sentences[1:], vectors[1:]):
    similarity = cosine_similarity(vectors[0], vector)
    print(f"  {similarity:.3f}  {sentence}")

print("\nสังเกต: ประโยคที่ 2 ไม่มีคำว่า 'ลาป่วย' หรือ 'ใบรับรองแพทย์' เลย แต่คะแนนสูงสุด")
print("เพราะ embedding เทียบที่ 'ความหมาย' ไม่ใช่เทียบคำตรงๆ แบบ SQL LIKE '%...%'")
