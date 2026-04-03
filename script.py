import re
import json
import os
import shutil  # для копіювання файлів

plants = {
    "Рослина": {
        "color": "#80d81b",
        "description": "Зона потрібних рослин. Без конкретики.",
    },
    "Гаультерія": {
        "color": "#8b4513",
        "description": "Зона гаультерії.",
    },
    "Американський женшень": {
        "color": "#c41e1e",
        "description": "Зона американського женшеню.",
    },
    "Корінь лопуха": {
        "color": "#836953",
        "description": "Зона кореню лопуха.",
    },
    "Мімоза соромлива": {
        "color": "#ffb6c1",
        "description": "Зона мімози соромливої.",
    },
    "Гіркий бур'ян": {
        "color": "#6b8f23",
        "description": "Зона гіркого бур'яну.",
    },
    "Шавлія пустельна": {
        "color": "#6b65a4",
        "description": "Зона шавлії пустельної.",
    },
    "Степовий мак": {
        "color": "#ffdd00",
        "description": "Зона степового маку.",
    },
    "Аляскинський женшень": {
        "color": "#da220a",
        "description": "Зона аляскинського женшеню.",
    },
    "Дикий білоцвіт": {
        "color": "#f0f0f0",
        "description": "Зона дикого білоцвіту.",
    },
    "Кровоцвіт": {
        "color": "#e2941c",
        "description": "Зона кровоцвіту.",
    },
    "Ахілея": {
        "color": "#ccd700",
        "description": "Зона ахілеї.",
    },
    "Деревій": {
        "color": "#ff4500",
        "description": "Зона деревію.",
    },
    "Молочай": {
        "color": "#8539e0",
        "description": "Зона молочаю.",
    },
    # "Шавлія покривальцева": {"color": "#9b30ff"},
    # "Дика м'ята": {"color": "#4caf50"},
    # "Дикий ревінь": {"color": "#8b0000"},
    # "Орегано": {"color": "#228b22"},
    # "Дубовик": {"color": "#d2b48c"},
    # "Ожина": {"color": "#4b0082"},
    # "Чорна смородина": {"color": "#2f2f4f"},
    # "Лохина": {"color": "#4169e1"},
    # "Червона Малина": {"color": "#d21f3c"},
    # "Золотиста смородина": {"color": "#da9650"},
}

plant_names = list(plants.keys())

json_file = "dusty_plants.json"
txt_file = "dusty_plants.txt"

if not os.path.exists(json_file):
    with open(json_file, "w", encoding="utf-8") as f:
        f.write("[]")

while True:
    coord_text = input(
        "\nВстав текст з координатами (приклад: Latitude: -**.*** / Longitude: **.***): "
    )

    match = re.search(
        r"Latitude:\s*([-0-9.]+)\s*/\s*Longitude:\s*([-0-9.]+)", coord_text
    )

    if not match:
        print("Не знайдено координати")
        continue

    lat = float(match.group(1))
    lng = float(match.group(2))

    print("\nОберіть рослину:")
    # 1 - щоб список починався з 1, а не 0
    for i, name in enumerate(plant_names, 1):
        print(f"{i}. {name}")

    try:
        plant_choice = int(input("Введи номер рослини: "))
        title = plant_names[plant_choice - 1]
    except:
        print("Неправильний вибір")
        continue

    plant = plants[title]

    new_entry = {
        "lat": lat,
        "lng": lng,
        "title": title,
        "description": plant["description"],
        "shape": "default",
        "icon": "plants",
        "color": plant["color"],
    }

    # читаємо файл
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # перевірка на дублікати
    duplicate_index = None
    for i, item in enumerate(data):
        if item["lat"] == lat and item["lng"] == lng:
            duplicate_index = i
            break

    if duplicate_index is not None:
        print(
            f"\nТака точка вже існує: {data[duplicate_index]['title']} ({lat}, {lng})"
        )
        overwrite = input("Enter - перезаписати, Ввести любий текст - пропустити: ").strip().lower()
        if overwrite == "":
            # перезаписуємо існуючий запис
            data[duplicate_index] = new_entry
            print("Запис перезаписано")
        else:
            print("Запис залишено без змін")
            continue
    else:
        # додаємо новий запис, якщо все ок
        data.append(new_entry)

    # очищаємо дублікати
    before = len(data)

    unique = []
    seen = set()

    for item in data:
        key = (item["lat"], item["lng"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    data = unique

    after = len(data)
    removed = before - after
    if removed > 0:
        print(f"Видалено дублікатів: {removed}")

    # сортуємо за порядком plants
    plant_order = list(plants.keys())
    data.sort(
        key=lambda x: (
            plant_order.index(x["title"])
            if x["title"] in plant_order
            else len(plant_order)
        )
    )

    # записуємо назад у JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # копіюємо в TXT
    shutil.copyfile(json_file, txt_file)

    # перезаписуємо TXT компактно
    with open(txt_file, "r", encoding="utf-8") as f:
        txt_data = json.load(f)

    with open(txt_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    print(f"\nДодано: ({lat}, {lng})")
    print(f"Файл {txt_file} оновлено, як копію JSON для мапи.")
