import re
import json
import os
import shutil  # для копіювання файлів

plants_config = {
    "Аляскинський Женшень": {"id": 0, "color": "#da220a"},
    "Гіркий бур'ян": {"id": 0, "color": "#6b8f23"},
    "Шавлія пустельна": {"id": 0, "color": "#6b65a4"},
    "Дикий білоцвіт": {"id": 0, "color": "#f0f0f0"},
    "Гаультерія": {"id": 0, "color": "#8b4513"},
    "Кровоцвіт": {"id": 0, "color": "#e2941c"},
    "Корінь лопуха": {"id": 0, "color": "#836953"},
    "Ахілея": {"id": 0, "color": "#ccd700"},
    "Деревій": {"id": 0, "color": "#ff4500"},
    "Молочай": {"id": 0, "color": "#8539e0"},
    "Мімоза соромлива": {"id": 0, "color": "#ffb6c1"},
    "Степовий мак": {"id": 0, "color": "#ffdd00"},
    "Шавлія покривальцева": {"id": 0, "color": "#9b30ff"},
    "Дика м'ята": {"id": 0, "color": "#4caf50"},
    "Дикий ревінь": {"id": 0, "color": "#8b0000"},
    "Орегано": {"id": 0, "color": "#228b22"},
    "Гриб: Дубовик": {"id": 0, "color": "#d2b48c"},
    "Ягода: Ожина": {"id": 0, "color": "#4b0082"},
    "Ягода: Чорна смородина": {"id": 0, "color": "#2f2f4f"},
    "Ягода: Лохина": {"id": 0, "color": "#4169e1"},
    "Ягода: Червона Малина": {"id": 0, "color": "#d21f3c"},
    "Ягода: Золотиста смородина": {"id": 0, "color": "#da9650"},
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

    # сортуємо за порядком plants_config
    plant_order = list(plants_config.keys())
    data.sort(key=lambda x: plant_order.index(x["title"]) if x["title"] in plant_order else len(plant_order))

    # записуємо назад у JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # робимо копію у TXT
    shutil.copyfile(json_file, txt_file)

    print(f"\nДодано: {title} ({lat}, {lng})")
    print(f"Файл {txt_file} оновлено, як копію JSON для мапи.")