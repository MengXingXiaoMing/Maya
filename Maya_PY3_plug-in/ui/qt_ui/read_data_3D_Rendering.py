# coding=gbk
import mmap
import os
import pickle  # 需要导入pickle模块


def read_from_shared_memory(shared_file=os.path.join("D:", "Personal", "zhankangming", "Desktop", "shared_mem.bin")):
    if not os.path.exists(shared_file):
        print("Shared memory file not found.")
        return None
    try:
        with open(shared_file, "r+b") as f:
            with mmap.mmap(f.fileno(), 0) as mm:
                mm.seek(0)
                # 读取数据长度（前4字节）
                data_size_bytes = mm.read(4)
                data_size = int.from_bytes(data_size_bytes, byteorder='big')

                # 读取实际数据
                data_bytes = mm.read(data_size)

                # 使用pickle反序列化，而不是UTF-8解码
                data = pickle.loads(data_bytes)

                print(f"Data read from shared memory: {data}")
                return data
    except Exception as e:
        print(f"Error reading shared memory: {e}")
        return None


read_from_shared_memory()