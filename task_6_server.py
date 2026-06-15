import socket
import threading
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 6666

def encrypt(data, key=77):
    result = bytearray()
    for b in data:
        b = ((b << 2) | (b >> 6)) & 0xFF
        b = b ^ key
        result.append(b)
    return bytes(result)

def check_json(text):
    stack = []
    for ch in text:
        if ch in '{[':
            stack.append(ch)
        elif ch == '}':
            if not stack or stack[-1] != '{':
                return False
            stack.pop()
        elif ch == ']':
            if not stack or stack[-1] != '[':
                return False
            stack.pop()
    return len(stack) == 0

def check_xml(text):
    stack = []
    i = 0
    while i < len(text):
        if text[i] == '<':
            j = text.find('>', i)
            if j == -1:
                return False
            tag = text[i+1:j]
            if not tag.startswith('/') and not tag.startswith('?') and not tag.startswith('!--'):
                stack.append(tag)
            elif tag.startswith('/'):
                tag_name = tag[1:]
                if not stack or stack[-1] != tag_name:
                    return False
                stack.pop()
            i = j
        i += 1
    return len(stack) == 0

def handle_client(conn, addr):
    print(f"Клиент подключён: {addr}")

    try:
        data = conn.recv(65536).decode('utf-8')
        if not data:
            conn.close()
            return

        parts = data.split('|', 2)
        cmd = parts[0]

        if cmd == "UPLOAD":
            filename = parts[1]
            content = parts[2] if len(parts) > 2 else ""

            print(f"  Получен файл: {filename}")
            print(f"  Размер: {len(content)} байт")

            if filename.endswith('.json'):
                if not check_json(content):
                    conn.send("ERROR|JSON not valid".encode())
                    conn.close()
                    return
            elif filename.endswith('.xml'):
                if not check_xml(content):
                    conn.send("ERROR|XML not valid".encode())
                    conn.close()
                    return
            else:
                conn.send("ERROR|Only JSON or XML".encode())
                conn.close()
                return

            os.makedirs("resources", exist_ok=True)
            with open(f"resources/{filename}", 'w', encoding='utf-8') as f:
                f.write(content)

            with open(f"resources/{filename}", 'rb') as f:
                file_data = f.read()

            encrypted = encrypt(file_data)
            with open(f"resources/{filename}.bin", 'wb') as f:
                f.write(encrypted)

            conn.send(f"OK|{filename}.bin saved".encode())
            print(f" Загружен: {filename}")

        elif cmd == "DOWNLOAD":
            filename = parts[1]
            filepath = f"resources/{filename}"

            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    conn.send(f.read())
                print(f" Отправлен: {filename}")
            else:
                conn.send(b"NOT_FOUND")
                print(f" Не найден: {filename}")

    except Exception as e:
        print(f"  Ошибка: {e}")
        conn.send(f"ERROR|{e}".encode())

    finally:
        conn.close()

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"Server on {SERVER_HOST}:{SERVER_PORT}")
    print("-" * 40)
    print("Ожидание подключений...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start()