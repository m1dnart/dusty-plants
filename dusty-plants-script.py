import re
import json
import os
import shutil  # для копіювання файлів

plants_config = {
    "Золотиста смородина": {"id": 0, "color": "#da9650"},
    "Аляскинський Женшень": {"id": 0, "color": "#da220a"},
    "Молочай": {"id": 0, "color": "#8539e0"},
    "Кровоцвіт": {"id": 0, "color": "#e2941c"},
    "Шавлія пустельна": {"id": 0, "color": "#6b65a4"},
}

plant_names = list(plants_config.keys())

json_file = "dusty_plants.json"
txt_file = "dusty_plants.txt"

if not os.path.exists(json_file):
    with open(json_file, "w", encoding="utf-8") as f:
        f.write("[]")

while True:
    text = input("\nВстав текст з координатами: ")

    match = re.search(r"Latitude:\s*([-0-9.]+)\s*/\s*Longitude:\s*([-0-9.]+)", text)

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
        choice = int(input("Введи номер: "))
        title = plant_names[choice - 1]
    except:
        print("Неправильний вибір")
        continue

    config = plants_config[title]

    new_entry = {
        "lat": lat,
        "lng": lng,
        "id": config["id"],
        "title": title,
        "description": "Dusty",
        "shape": "default",
        "icon": "plants",
        "color": config["color"]
    }

    # читаємо файл
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # перевірка на дублікати
    duplicate = False
    for item in data:
        if item["lat"] == lat and item["lng"] == lng:
            duplicate = True
            break

    if duplicate:
        print("\nТака точка вже існує!")
        continue

    # додаємо новий запис, якщо все ок
    data.append(new_entry)

    # записуємо назад у JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # робимо копію у TXT
    shutil.copyfile(json_file, txt_file)

    print(f"\nДодано: {title} ({lat}, {lng})")
    print(f"Файл {txt_file} оновлено, як копію JSON для мапи.")