
import asyncio
import threading
import multiprocessing
import time
import struct
import zlib
import marshal
import base64
from io import BytesIO
import os
from types import ModuleType

# 1) Singleton Decorator — ทำให้คลาสมีได้แค่ instance เดียวในระบบ
def singleton(cls):  # decorator รับ class
    instances = {}   # เก็บ instance เดียวของแต่ละ class

    def get_instance(*args, **kwargs):  # ฟังก์ชัน wrapper
        if cls not in instances:        # หากยังไม่เคยสร้าง
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]           # คืนค่าตัวเดียวเสมอ
    return get_instance


# 2) Custom Metaclass — บังคับว่าคลาสไหนใช้ ต้องมี method ชื่อ run()
class RequireRun(type):  # metaclass
    def __new__(m, name, bases, attrs):
        if "run" not in attrs:
            raise TypeError(f"คลาส {name} ต้องมีฟังก์ชัน run()")  # เงื่อนไขบังคับ
        return super().__new__(m, name, bases, attrs)


# 3) EventBus — ระบบส่ง event ภายในโปรแกรม (คล้าย pub/sub)
@singleton
class EventBus:
    def __init__(self):
        self.listeners = {}  # เก็บ event : callback list

    def subscribe(self, event, fn):
        self.listeners.setdefault(event, []).append(fn)  # ผูก callback

    def emit(self, event, data):
        for fn in self.listeners.get(event, []):
            fn(data)  # เรียก callback พร้อมข้อมูล


# 4) Context Manager — จัดการ Resource ปลอม (จำลองไฟล์/DB)
class FakeResource:
    def __enter__(self):
        print("🔓 เปิด resource")
        return "RESOURCE_DATA"   # ส่งค่าให้ตัวแปรใน with

    def __exit__(self, exc_type, exc, tb):
        print("🔒 ปิด resource")
        return False   # ให้ exception ส่งต่อ (ไม่กลืน error)


# 5) Generator ขั้นสูง — ใช้ pipeline Streaming
def data_stream():
    for i in range(5):
        yield i * 2               # ส่งค่าเป็น stream (lazy evaluate)


# 6) Iterator Protocol แบบเต็ม
class Counter:
    def __init__(self, limit):
        self.current = 0
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):  # ถูกเรียกทุกครั้งเมื่อวนลูป
        if self.current >= self.limit:
            raise StopIteration
        self.current += 1
        return self.current


# 7) Compression Pipeline (marshal + zlib + base64)
#    ใช้จริงในระบบ obfuscate
def encode_data(obj):
    raw = marshal.dumps(obj)          # แปลงเป็น bytecode
    comp = zlib.compress(raw)         # บีบอัดข้อมูล
    return base64.b64encode(comp)     # เข้ารหัส base64


def decode_data(encoded):
    comp = base64.b64decode(encoded)
    raw = zlib.decompress(comp)
    return marshal.loads(raw)


# 8) ใช้ struct pack/unpack เพื่อจัดการ binary ระดับต่ำ
def pack_binary(num, fl):
    return struct.pack("if", num, fl)  # i=int, f=float


def unpack_binary(data):
    return struct.unpack("if", data)


# 9) Async Task แบบลึกจัด
async def async_task(name):
    print(f"เริ่ม async {name}")
    await asyncio.sleep(1)
    print(f"จบ async {name}")


# 10) Thread Function
def thread_job():
    print("Thread ทำงาน…")
    time.sleep(1)


# 11) Process Function
def process_job():
    print("Process ทำงาน…")
    time.sleep(1)


# 12) Dynamic Import Module In-Memory
def load_module_from_string(code, module_name):
    module = ModuleType(module_name)
    exec(code, module.__dict__)       # โหลด code เข้า module
    return module


# 13) Class ขั้นสูง ใช้ metaclass RequireRun
class AdvancedSystem(metaclass=RequireRun):
    def run(self):
        print("ระบบกำลังทำงาน…")


# 14) Pattern Matching ระดับสูง (Python 3.10+)
def match_demo(x):
    match x:
        case {"type": "error", "code": c}:
            print("Error code =", c)
        case [a, b]:
            print("List length 2 =", a, b)
        case _:
            print("อื่นๆ")


# 15) MAIN — รวมการทำงานทุกอย่างเข้าด้วยกัน
def main():

    # Context Manager
    with FakeResource() as r:
        print("ใช้งาน resource =", r)

    # Generator
    print("DATA STREAM:", list(data_stream()))

    # Iterator
    print("ITERATOR:", list(Counter(5)))

    # Encode / Decode
    encoded = encode_data({"hello": 123})
    print("ENCODED:", encoded)
    print("DECODED:", decode_data(encoded))

    # Struct binary
    binary = pack_binary(99, 1.23)
    print("UNPACK:", unpack_binary(binary))

    # EventBus
    bus = EventBus()
    bus.subscribe("hello", lambda d: print("EVENT รับค่า:", d))
    bus.emit("hello", {"msg": "สวัสดี"})

    # Async
    asyncio.run(async_task("T1"))

    # Thread
    t = threading.Thread(target=thread_job)
    t.start()
    t.join()

    # Process
    p = multiprocessing.Process(target=process_job)
    p.start()
    p.join()

    # Pattern matching
    match_demo({"type": "error", "code": 404})

    # Dynamic module
    mod = load_module_from_string("def hi(): print('HI FROM MEMORY')", "MemoryMod")
    mod.hi()

    # Metaclass class
    system = AdvancedSystem()
    system.run()


main()