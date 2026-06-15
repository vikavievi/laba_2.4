with open("resources/data.bin", "wb") as f:
    f.write(b'DATA')  # сигнатура
    f.write((1).to_bytes(2, 'little'))  # версия
    f.write((3).to_bytes(4, 'little'))  # количество записей

    # запись 1
    f.write((1000).to_bytes(8, 'little'))  # время
    f.write((101).to_bytes(4, 'little'))  # ID
    f.write((2300).to_bytes(2, 'little', signed=True))  # температура 23.00
    f.write((1).to_bytes(1, 'little'))  # флаг (активный)

    # запись 2
    f.write((200).to_bytes(8, 'little'))
    f.write((102).to_bytes(4, 'little'))
    f.write((-500).to_bytes(2, 'little', signed=True))
    f.write((0).to_bytes(1, 'little'))

    # запись 3
    f.write((300).to_bytes(8, 'little'))
    f.write((103).to_bytes(4, 'little'))
    f.write((1850).to_bytes(2, 'little', signed=True))
    f.write((3).to_bytes(1, 'little'))

print("Файл data.bin создан!")
print()

file = open("resources/data.bin", "rb")
signature = file.read(4)
version_bytes = file.read(2)
version = int.from_bytes(version_bytes, 'little')
count_bytes = file.read(4)
num_records = int.from_bytes(count_bytes, 'little')

print("Подпись:", signature)
print("Версия:", version)
print("Количество записей:", num_records)

total_temp = 0
active_count = 0

for i in range(num_records):
    time_bytes = file.read(8)
    timestamp = int.from_bytes(time_bytes, 'little')

    id_bytes = file.read(4)
    record_id = int.from_bytes(id_bytes, 'little')

    temp_bytes = file.read(2)
    temp_raw = int.from_bytes(temp_bytes, 'little', signed=True)
    temperature = temp_raw / 100

    flag = file.read(1)[0]

    total_temp = total_temp + temperature

    if flag & 1:
        active_count = active_count + 1

    print(f"\nЗапись {i + 1}:")
    print(f"  Время: {timestamp}")
    print(f"  ID: {record_id}")
    print(f"  Температура: {temperature}°C")
    print(f"  Флаг: {flag}")

average = total_temp / num_records
print("СТАТИСТИКА:")
print("Средняя температура:", average, "°C")
print("Количество активных флагов:", active_count)

file.close()