import re
import json
import os
import shutil  # для копіювання файлів

json_file = "dusty_plants.json"
txt_file = "dusty_plants.txt"

if not os.path.exists(json_file):
    with open(json_file, "w", encoding="utf-8") as f:
        f.write("[]")

while True:
    text = input("\nВстав текст з координатами (приклад: Latitude: -**.*** / Longitude: **.***): ")

    match = re.search(r"Latitude:\s*([-0-9.]+)\s*/\s*Longitude:\s*([-0-9.]+)", text)

    if not match:
        print("Не знайдено координати")
        continue

    lat = float(match.group(1))
    lng = float(match.group(2))

    new_entry = {
        "lat": lat,
        "lng": lng,
        "id": 0,
        "title": "Plant",
        "description": "Dusty",
        "shape": "default",
        "icon": "plants",
        "color": "#da220a"
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
    
    # записуємо назад у JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # компактникй TXT
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    print(f"\nДодано: ({lat}, {lng})")
    print(f"Файл {txt_file} оновлено, як копію JSON для мапи.")