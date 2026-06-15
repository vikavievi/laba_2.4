import re
import os

class SimpleXML:

    @staticmethod
    def serialize(obj, root_name="root", indent=0, level=0):
        # сериализация
        spaces = " " * (indent * level) if indent else ""
        next_spaces = " " * (indent * (level + 1)) if indent else ""

        if isinstance(obj, dict):
            if not obj:
                return f"{spaces}<{root_name}/>"

            result = f"{spaces}<{root_name}>\n"
            for key, value in obj.items():
                if key.startswith('@'):
                    continue
                result += SimpleXML.serialize(value, key, indent, level + 1)
            result += f"{spaces}</{root_name}>"
            return result

        elif isinstance(obj, list):
            result = ""
            for item in obj:
                result += SimpleXML.serialize(item, root_name, indent, level)
            return result

        else:
            if indent:
                return f"{spaces}<{root_name}>{str(obj)}</{root_name}>\n"
            return f"<{root_name}>{str(obj)}</{root_name}>"

    @staticmethod
    def deserialize(xml_str):
        # десериализация
        xml_str = xml_str.strip()
        xml_str = re.sub(r'<!--.*?-->', '', xml_str, flags=re.DOTALL)

        match = re.match(r'<([^>\s]+)([^>]*)>', xml_str)
        if not match:
            return None

        root_name = match.group(1)
        attrs_str = match.group(2)
        close_tag = f"</{root_name}>"
        end_pos = xml_str.rfind(close_tag)
        if end_pos == -1:
            return None

        content = xml_str[len(match.group(0)):end_pos].strip()

        if not content:
            return None

        result = {}
        if attrs_str:
            attrs = re.findall(r'(\w+)=["\']([^"\']*)["\']', attrs_str)
            for attr_name, attr_value in attrs:
                result[f"@{attr_name}"] = attr_value

        children = SimpleXML._parse_children(content)

        if not children and not re.search(r'<[^>]+>', content):
            return content.strip()

        for child_name, child_value in children:
            if child_name in result:
                if not isinstance(result[child_name], list):
                    result[child_name] = [result[child_name]]
                result[child_name].append(child_value)
            else:
                result[child_name] = child_value

        return result

    @staticmethod
    def _parse_children(xml_str):
        children = []
        pattern = re.compile(r'<([^>\s]+)([^>]*)>(.*?)</\1>', re.DOTALL)

        for match in pattern.finditer(xml_str):
            tag_name = match.group(1)
            content = match.group(3).strip()

            nested = SimpleXML._parse_children(content)

            if nested:
                value = {}
                for k, v in nested:
                    if k in value:
                        if not isinstance(value[k], list):
                            value[k] = [value[k]]
                        value[k].append(v)
                    else:
                        value[k] = v
            else:
                value = content if content else None

            children.append((tag_name, value))

        return children

    @staticmethod
    def validate(xml_str):
        stack = []
        lines = xml_str.split('\n')
        in_comment = False

        for line_num, line in enumerate(lines, 1):
            pos = 0
            length = len(line)

            while pos < length:
                if line[pos:pos+4] == '<!--':
                    in_comment = True
                    pos += 4
                    continue
                if in_comment and line[pos:pos+3] == '-->':
                    in_comment = False
                    pos += 3
                    continue
                if in_comment:
                    pos += 1
                    continue

                if line[pos] == '<' and pos + 1 < length and line[pos+1] != '/':
                    if line[pos+1] == '?':
                        pos += 1
                        continue

                    end = line.find('>', pos)
                    if end == -1:
                        return False, line_num, pos + 1

                    tag = line[pos+1:end].split()[0]
                    stack.append((tag, line_num, pos + 1))
                    pos = end + 1

                elif line[pos] == '<' and pos + 1 < length and line[pos+1] == '/':
                    end = line.find('>', pos)
                    if end == -1:
                        return False, line_num, pos + 1

                    tag = line[pos+2:end].strip()
                    if not stack or stack[-1][0] != tag:
                        return False, line_num, pos + 1
                    stack.pop()
                    pos = end + 1
                else:
                    pos += 1

        if stack:
            tag, line_num, col = stack[-1]
            return False, line_num, col

        return True, 0, 0


print("ПРОВЕРКА XML ФАЙЛОВ ИЗ РЕПОЗИТОРИЯ RetmixX/test_objects")

xml_files = [
    "test_1.xml",
    "test_2.xml",
    "test_3.xml",
    "test_4.xml",
    "test_5.xml",
    "test_6.xml",
    "test_7.xml",
]

print("\nФайлы для проверки:", ", ".join(xml_files))

for filename in xml_files:
    print(f"\n--- {filename} ---")

    if not os.path.exists(filename):
        print(f"Файл не найден! Скачайте из репозитория")
        continue

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # валидация
    is_valid, line, col = SimpleXML.validate(content)
    if is_valid:
        print(f"ВАЛИДАЦИЯ: ПРОЙДЕНА")
        # десериализация
        try:
            result = SimpleXML.deserialize(content)
            print(f"ДЕСЕРИАЛИЗАЦИЯ: УСПЕШНА")
            print(f"Содержимое: {result}")
        except Exception as e:
            print(f"ДЕСЕРИАЛИЗАЦИЯ: ОШИБКА - {e}")
    else:
        print(f"ВАЛИДАЦИЯ: ОШИБКА на строке {line}, позиция {col}")

print('\n', "=" * 20)
print("ПРОВЕРКА ЗАВЕРШЕНА")
