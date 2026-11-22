"""ฟังก์ชันที่ใช้ร่วมกันใน Week 2 (RAG)

เทียบ C#: ไฟล์นี้เหมือน class library เล็กๆ ที่สคริปต์ 05 กับ 06 เรียกใช้ (import rag_utils)
"""

import json
import math
import sys
from pathlib import Path

import ollama

# Windows: stdout/stdin เป็น cp1252 ทำให้ print/input ภาษาไทยพัง บังคับ UTF-8 ไว้เลย
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

CHAT_MODEL = "qwen2.5:3b"
EMBEDDING_MODEL = "bge-m3"  # โมเดลแปลงข้อความเป็นตัวเลข รองรับภาษาไทย

DATA_FOLDER = Path(__file__).parent / "data"
INDEX_FILE = Path(__file__).parent / "index.json"


def load_documents(folder=DATA_FOLDER):
    """อ่านไฟล์ .md ทุกไฟล์ในโฟลเดอร์ data คืนค่าเป็น list ของ {"source", "text"}"""
    documents = []
    for file_path in sorted(folder.glob("*.md")):
        documents.append({"source": file_path.name, "text": file_path.read_text(encoding="utf-8")})
    return documents


def split_into_chunks(document):
    """หั่นเอกสารเป็นชิ้นตามหัวข้อ "## "

    ภาษาไทยไม่เว้นวรรคระหว่างคำ ตัดตามหัวข้อง่ายและได้ชิ้นที่มีความหมายครบกว่าตัดตามจำนวนตัวอักษร
    ใส่ชื่อเอกสาร (บรรทัด "# ") ไว้หน้าทุกชิ้น ให้แต่ละชิ้นรู้ว่ามาจากเรื่องอะไร
    """
    lines = document["text"].splitlines()
    document_title = lines[0].lstrip("# ").strip()

    chunks = []
    current_section_lines = []
    for line in lines[1:]:
        if line.startswith("## ") and current_section_lines:
            chunks.append(current_section_lines)
            current_section_lines = []
        current_section_lines.append(line)
    if current_section_lines:
        chunks.append(current_section_lines)

    result = []
    for section_lines in chunks:
        section_text = "\n".join(section_lines).strip()
        if section_text:
            result.append({"source": document["source"], "text": f"{document_title}\n{section_text}"})
    return result


def embed_texts(texts):
    """แปลง list ของข้อความ เป็น list ของ vector (list ของตัวเลข) ด้วย embedding model"""
    response = ollama.embed(model=EMBEDDING_MODEL, input=texts)
    return response["embeddings"]


def cosine_similarity(vector_a, vector_b):
    """วัดว่า 2 vector ชี้ไปทางเดียวกันแค่ไหน: ใกล้ 1 = ความหมายใกล้กัน, ใกล้ 0 = ไม่เกี่ยวกัน"""
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    length_a = math.sqrt(sum(a * a for a in vector_a))
    length_b = math.sqrt(sum(b * b for b in vector_b))
    return dot_product / (length_a * length_b)


def build_index():
    """อ่านเอกสาร -> หั่นเป็นชิ้น -> แปลงแต่ละชิ้นเป็น vector -> คืนค่าเป็น "index" (list ของชิ้น + vector)"""
    all_chunks = []
    for document in load_documents():
        all_chunks.extend(split_into_chunks(document))

    chunk_vectors = embed_texts([chunk["text"] for chunk in all_chunks])
    for chunk, vector in zip(all_chunks, chunk_vectors):
        chunk["vector"] = vector
    return all_chunks


def load_or_build_index():
    """ถ้ามี index.json แล้วและเอกสารไม่เปลี่ยน ใช้ของเดิม ไม่ต้อง embed ใหม่ (เร็วขึ้นมาก)"""
    newest_document_time = max(path.stat().st_mtime for path in DATA_FOLDER.glob("*.md"))
    if INDEX_FILE.exists() and INDEX_FILE.stat().st_mtime > newest_document_time:
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))

    print("กำลังสร้าง index จากเอกสารใน data/ ...")
    index = build_index()
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    print(f"สร้าง index เสร็จ: {len(index)} ชิ้น บันทึกไว้ที่ {INDEX_FILE.name}\n")
    return index


def search(index, question, top_k=3):
    """หาชิ้นเอกสารที่ความหมายใกล้คำถามที่สุด top_k ชิ้น (นี่คือตัว "R" = Retrieval ใน RAG)"""
    question_vector = embed_texts([question])[0]
    scored_chunks = []
    for chunk in index:
        score = cosine_similarity(question_vector, chunk["vector"])
        scored_chunks.append({"source": chunk["source"], "text": chunk["text"], "score": score})
    scored_chunks.sort(key=lambda chunk: chunk["score"], reverse=True)
    return scored_chunks[:top_k]


def build_context(found_chunks):
    """เอาชิ้นเอกสารที่ค้นเจอมาต่อกันเป็นข้อความเดียว เพื่อแปะลงใน prompt"""
    return "\n\n---\n\n".join(f"[{chunk['source']}]\n{chunk['text']}" for chunk in found_chunks)


RAG_SYSTEM_PROMPT = """คุณเป็นผู้ช่วยฝ่ายบุคคลของบริษัท นาวาเทค โซลูชั่น
ตอบคำถามโดยใช้ข้อมูลใน "เอกสารอ้างอิง" ที่ให้มาเท่านั้น ตอบเป็นภาษาไทย กระชับ ระบุตัวเลขให้ชัด
ถ้าในเอกสารไม่มีคำตอบ ให้ตอบว่า "ไม่พบข้อมูลนี้ในเอกสารของบริษัท" ห้ามเดาเอง"""
