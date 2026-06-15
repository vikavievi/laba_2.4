import socket
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 6666


def upload_file(filepath):
    if not os.path.exists(filepath):
        print(f" Файл не найден: {filepath}")
        return

    filename = os.path.basename(filepath)

    if not (filename.endswith('.json') or filename.endswith('.xml')):
        print(" Можно загружать только .json или .xml файлы")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\n Загрузка файла: {filename}")
    print(f"   Размер: {len(content)} байт")

    message = f"UPLOAD|{filename}|{content}"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    client.send(message.encode('utf-8'))

    response = client.recv(4096).decode()
    print(f" Ответ сервера: {response}")
    client.close()


def download_file(filename):
    print(f"\n Скачивание файла: {filename}")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))

    client.send(f"DOWNLOAD|{filename}".encode())

    data = client.recv(65536)

    if data == b"NOT_FOUND":
        print(" Файл не найден на сервере")
        client.close()
        return

    os.makedirs("downloads", exist_ok=True)
    with open(f"downloads/{filename}", 'wb') as f:
        f.write(data)

    print(f" Файл сохранён: downloads/{filename}")
    print(f" Размер: {len(data)} байт")
    client.close()


def list_files():
    print("\n Файлы на сервере (папка resources):")

    if not os.path.exists("resources"):
        print(" Папка resources не найдена!")
        print(" Сначала загрузите файл через команду 1")
        return

    files = os.listdir("resources")

    if not files:
        print(" Папка resources пуста")
        return

    for f in sorted(files):
        size = os.path.getsize(f"resources/{f}")
        if f.endswith('.bin'):
            print(f" {f} ({size} байт)")
        else:
            print(f" {f} ({size} байт)")

def main():
    print("КЛИЕНТ ДЛЯ РАБОТЫ С СЕРВЕРОМ")
    print(f"Сервер: {SERVER_HOST}:{SERVER_PORT}")
    print()

    while True:
        print("-" * 30)
        print("Выберите действие:")
        print("1. Загрузить JSON/XML файл на сервер")
        print("2. Скачать бинарный файл с сервера")
        print("3. Показать файлы на сервере")
        print("4. Выход")

        choice = input("Ваш выбор (1-4): ").strip()

        if choice == '1':
            path = input("Путь к файлу (например, test.json): ")
            upload_file(path)
        elif choice == '2':
            filename = input("Имя файла на сервере (например, test.json.bin): ")
            download_file(filename)
        elif choice == '3':
            list_files()
        elif choice == '4':
            print(" Аривидерчи!")
            break
        else:
            print(" Неверный выбор")


if __name__ == "__main__":
    main()