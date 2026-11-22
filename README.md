# LLM Week 1 — เรียก LLM ในเครื่องตัวเองด้วย Python + Ollama

เป้าหมายสัปดาห์นี้: ให้คุณรันโค้ดที่ "คุยกับ AI" บนเครื่องตัวเองได้ ฟรี ไม่ต้องสมัคร API key
และเข้าใจว่าการเรียก LLM ก็คือการยิง HTTP API ธรรมดาที่คุณทำอยู่แล้วทุกวัน

## สิ่งที่ต้องติดตั้ง (ทำครั้งเดียว)

### 1. Python

**Windows:**
```powershell
winget install Python.Python.3.12
```
ปิดแล้วเปิด terminal ใหม่ แล้วเช็ค: `python --version`

### 2. Ollama (ตัวรัน LLM ในเครื่อง ฟรี)

โหลดที่ [ollama.com/download](https://ollama.com/download) แล้วลงตัวติดตั้งเหมือนโปรแกรมทั่วไป
(Windows ติดตั้งแล้วจะรันเองใน background)

ดึงโมเดลขนาดเล็ก (~1.9 GB) — qwen2.5 เล่นภาษาไทยได้ค่อนข้างดี:
```powershell
ollama pull qwen2.5:3b
```

ลองคุยกับมันตรงๆ เช็คว่าทำงาน:
```powershell
ollama run qwen2.5:3b "สวัสดี"
```

### 3. ติดตั้ง package ของโปรเจกต์

```powershell
cd <โฟลเดอร์ที่ clone repo นี้มา>
pip install -r requirements.txt
```

## รันตัวอย่าง (ทำตามลำดับ)

```powershell
python 01_call_api_raw.py        # เรียก LLM ด้วย HTTP เปล่าๆ ไม่มี library
python 02_ollama_package.py      # เรียกผ่าน package สำเร็จรูป
python 03_chat_with_history.py   # แชทวนลูป เห็นว่า "ความจำ" ของ LLM ทำงานยังไง
```

## ให้สังเกตอะไร

- **ตัวอย่าง 1:** การเรียก AI คือ `POST /api/generate` ส่ง JSON `{"model": ..., "prompt": ...}` — เหมือน API ที่คุณเขียนเองทุกวัน
- **ตัวอย่าง 2:** มี `role: "system"` สำหรับตั้งกฎให้โมเดล กับ `role: "user"` สำหรับคำถาม
- **ตัวอย่าง 3:** LLM **จำอะไรไม่ได้เลย** — เราต้องส่งประวัติแชททั้งหมดกลับไปทุกรอบ ลองถาม "ผมชื่อ Rachen" แล้วถามต่อว่า "ผมชื่ออะไร" จะเห็นว่ามันจำได้เพราะเราส่งประวัติกลับไป ไม่ใช่เพราะมันฉลาด

สิ่งที่ทำในตัวอย่าง 3 คือหัวใจของ RAG: สัปดาห์หน้าเราจะเอา "เอกสารที่ค้นมาได้" แทรกเข้า list เดียวกันนี้ ให้มันตอบจากเอกสารของเรา

## อ่าน Python เพิ่ม

[docs/python-for-csharp-dev.md](docs/python-for-csharp-dev.md) — สรุป Python เทียบ C# สำหรับคนเขียน .NET มา 10 ปี

## Troubleshooting

| ปัญหา | วิธีแก้ |
|---|---|
| `python` หาไม่เจอ (Windows) | ลอง `py` แทน หรือติดตั้ง Python ใหม่แล้วติ๊ก "Add to PATH" |
| `ollama` หาไม่เจอ | ติดตั้ง Ollama แล้วเปิด terminal ใหม่ (Windows รันเองอยู่แล้ว) |
| สคริปต์บอก connection refused | Ollama ไม่ได้รัน — พิมพ์ `ollama serve` ค้างไว้ใน terminal อีกอัน |
| โมเดลตอบช้า | เครื่องไม่มี GPU จะช้าหน่อย ปกติ รอได้; ถ้าช้ามากเปลี่ยนเป็น `qwen2.5:1.5b` (เล็กลง) โดยแก้ `MODEL_NAME` ในสคริปต์ |
| `pip install` error สีแดง | ลอง `python -m pip install -r requirements.txt` |
