with open("resources/numbers.txt", "w") as f:
    f.write("7\n")
    f.write("14\n")
    f.write("21\n")
    f.write("3\n")
    f.write("5\n")
    f.write("28\n")
    f.write("10\n")

print("ИСХОДНЫЙ ФАЙЛ numbers.txt:")
with open("resources/numbers.txt", "r") as f:
    print(f.read())

def process_file(input_file, output_file):
    denominator = 73 * 73 + 29  # 5358

    with open(input_file, "r") as f_in:
        lines = f_in.readlines()

    result_lines = []

    for line in lines:
        line = line.strip()

        if line == "":
            continue

        try:
            number = int(line)

            if number % 7 == 0:
                new_value = number * 100 / denominator
                result_lines.append(str(new_value) + "\n")
            else:
                result_lines.append(line + "\n")
        except:
            result_lines.append(line + "\n")

    with open(output_file, "w") as f_out:
        f_out.writelines(result_lines)

    print("Готово!")

process_file("resources/numbers.txt", "resources/numbers_new.txt")

print("\nРЕЗУЛЬТАТ В ФАЙЛЕ numbers_new.txt:")
with open("resources/numbers_new.txt", "r") as f:
    print(f.read())