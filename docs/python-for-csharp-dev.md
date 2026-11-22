# Python สำหรับคนเขียน C# — อ่าน 10 นาทีจบ

เทียบทีละอย่างกับที่คุ้นอยู่แล้ว

## ตัวแปรและชนิดข้อมูล

```python
# C#: var name = "Rachen"; / int age = 35;
name = "Rachen"          # ไม่ต้องประกาศชนิด ไม่มีเซมิโคลอน
age = 35
score = 8.5              # float
is_ready = True          # bool คือ True/False (ตัวใหญ่) ไม่ใช่ true/false
nothing = None           # null คือ None
```

## โครงสร้างข้อมูลที่ใช้บ่อยสุด

```python
# List<T> ใน C#
employees = ["Ann", "Bob"]
employees.append("Cat")        # .Add()
first_name = employees[0]      # index เหมือนกัน

# Dictionary<string, string>
config = {"model": "llama3.2", "host": "localhost"}
config["timeout"] = "30"       # เพิ่ม/แก้ค่า
model_name = config["model"]   # อ่านค่า
```

## Function

```python
# C#: string Greet(string name) { return $"Hi {name}"; }
def greet(name):
    return f"Hi {name}"        # f-string = $"..." ใน C# เลย
```

**จุดที่คน C# พลาดบ่อย:** Python ใช้ indent (ย่อหน้า) แทน `{ }` — ไม่มีปีกกา
scope คือการย่อหน้าเข้าไป เหมือน `if`/`for` ใน C# แต่ห้ามเว้นวรรคผิด

## if / for / while

```python
if age > 30:
    print("senior")
elif age > 20:
    print("junior")
else:
    print("intern")

for employee in employees:     # foreach (var employee in employees)
    print(employee)

for i in range(10):            # for (int i = 0; i < 10; i++)
    print(i)
```

## String

```python
text = "hello"
text.upper()                   # ToUpper()
text.split(",")                # Split()
f"age = {age}"                 # $"age = {age}"
text.strip()                   # Trim()
```

## class + method

```python
class ChatClient:
    def __init__(self, model_name):      # constructor
        self.model_name = model_name     # this.model_name

    def ask(self, question):             # method ต้องรับ self เป็น parameter แรกเสมอ
        return f"asked: {question}"

client = ChatClient("llama3.2")          # new ChatClient(...)
print(client.ask("hi"))
```

## import (เทียบกับ using + NuGet)

```python
import json                    # เหมือน using + reference built-in
import urllib.request          # ใช้เป็น urllib.request.Request(...)
from datetime import datetime  # import เฉพาะตัว
```

ติดตั้ง package ภายนอก: `pip install <name>` (เทียบกับ `dotnet add package`)
เก็บ list package ไว้ใน `requirements.txt` (เทียบกับ `<PackageReference>` ใน .csproj)
รันติดตั้งทั้งหมด: `pip install -r requirements.txt`

## อ่านโค้ดตัวอย่างในโปรเจกต์นี้

| C# | Python ที่จะเจอ |
|---|---|
| `Main()` entry point | `if __name__ == "__main__":` |
| `Dictionary` literal | `{"key": "value"}` ทุกอันที่เห็นเยอะๆ |
| `var response = await client.PostAsync(...)` | `urllib.request.urlopen(...)` หรือ `ollama.chat(...)` |
| `using (var x = ...)` | `with x as y:` |

## สิ่งที่ยังไม่ต้องสนใจตอนนี้

- `async/await` (Python มีเหมือนกัน แต่ตัวอย่างสัปดาห์นี้ไม่ใช้)
- decorator `@xxx`, type hint, virtual env — เจอเมื่อจำเป็น
- ตอนนี้เป้าหมายแค่อ่านสคริปต์ใน repo นี้แล้วแก้เล่นเองได้ ก็พอ
