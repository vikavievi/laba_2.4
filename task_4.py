import re
import os


class SimpleJSON:
    @staticmethod
    def stringify(obj, indent=0, level=0):
        spaces = "  " * (indent * level) if indent else ""
        inner_spaces = "  " * (indent * (level + 1)) if indent else ""

        if isinstance(obj, dict):
            if not obj:
                return "{}"
            items = []
            for k, v in obj.items():
                key = f'"{k}"'
                value = SimpleJSON.stringify(v, indent, level + 1)
                if indent:
                    items.append(f"{inner_spaces}{key}: {value}")
                else:
                    items.append(f"{key}:{value}")
            if indent:
                return "{\n" + ",\n".join(items) + f"\n{spaces}" + "}"
            return "{" + ",".join(items) + "}"

        elif isinstance(obj, list):
            if not obj:
                return "[]"
            items = [SimpleJSON.stringify(item, indent, level + 1) for item in obj]
            if indent:
                return "[\n" + ",\n".join(f"{inner_spaces}{item}" for item in items) + f"\n{spaces}]"
            return "[" + ",".join(items) + "]"

        elif isinstance(obj, str):
            return f'"{obj}"'
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif obj is None:
            return "null"
        elif isinstance(obj, (int, float)):
            return str(obj)
        else:
            return str(obj)

    @staticmethod
    def parse(json_str):
        json_str = json_str.strip()
        json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
        json_str = json_str.replace("true", "True").replace("false", "False").replace("null", "None")
        try:
            return eval(json_str)
        except Exception as e:
            raise ValueError(f"Ошибка парсинга JSON: {e}")

    @staticmethod
    def validate(json_str):
        stack = []
        in_string = False
        escape = False
        line = 1
        char_pos = 0

        for i, ch in enumerate(json_str):
            if ch == '\n':
                line += 1
                char_pos = 0
            else:
                char_pos += 1

            if not in_string:
                if ch in '{[':
                    stack.append(ch)
                elif ch == '}':
                    if not stack or stack[-1] != '{':
                        return False, line, char_pos
                    stack.pop()
                elif ch == ']':
                    if not stack or stack[-1] != '[':
                        return False, line, char_pos
                    stack.pop()
                elif ch == '"':
                    in_string = True
            else:
                if not escape and ch == '"':
                    in_string = False
                escape = (ch == '\\' and not escape)

        if in_string:
            return False, line, char_pos
        if len(stack) > 0:
            return False, line, char_pos
        return True, 0, 0


print("ПРОВЕРКА JSON ФАЙЛОВ ИЗ РЕПОЗИТОРИЯ")

test_files = [
    "test_1.json",
    "test_2.json",
    "test_3.json",
    "test_4.json",
    "test_5.json",
    "test_6.json",
    "test_7.json",
    "test_8.json",
    "test_9.json",
    "json_10.json"
]

for filename in test_files:
    print(f"\n--- {filename} ---")

    if not os.path.exists(filename):
        print(f"  Файл не найден!")
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    is_valid, line, pos = SimpleJSON.validate(content)
    if is_valid:
        print(f"  Валидация: ПРОЙДЕНА")

        try:
            result = SimpleJSON.parse(content)
            print(f"  Парсинг: УСПЕШНО")
        except Exception as e:
            print(f"  Парсинг: {e}")
    else:
        print(f"  Валидация: ОШИБКА на строке {line}, позиция {pos}")
print('\n',"=" * 20)
print("ПРОВЕРКА ЗАВЕРШЕНА")