import re
import json
import os
from datetime import datetime

json_file = "dusty_plants.json"
txt_file = "dusty_plants.txt"
plants_info_file = "plants_info.json"


def load_plants():
    if not os.path.exists(plants_info_file):
        raise FileNotFoundError(f"{plants_info_file} не знайдено!")
    with open(plants_info_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_data():
    if not os.path.exists(json_file):
        with open(json_file, "w", encoding="utf-8") as f:  # якщо немає, то створює json (dusty_tales.json)
            json.dump([], f, ensure_ascii=False)
    with open(json_file, "r", encoding="utf-8") as f:  # читання json
        return json.load(f)


def sync_txt_with_json(data):
    with open(txt_file, "w", encoding="utf-8") as f:  # по суті створення txt, на основі data
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def create_session_file(folder="dates"):
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{datetime.now().strftime('%d-%m-%Y_%H-%M')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")
    return filename


def update_session_file(session_file, session_data):
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Файл сесії {session_file} оновлено")


def save_data(data):
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    sync_txt_with_json(data)


def get_new_entry(plants):
    plant_names = list(plants.keys())
    while True:
        coord_text = input("\nВстав текст з координатами (приклад: Latitude: -**.*** / Longitude: **.***): ")
        match = re.search(r"Latitude:\s*([-0-9.]+)\s*/\s*Longitude:\s*([-0-9.]+)", coord_text)
        if not match:
            print("Не знайдено координати")
            continue
        lat = float(match.group(1))
        lng = float(match.group(2))
        break

    print("\nОбери рослину або просто натисни Enter, щоб позначити 'Відвідано':")
    for i, name in enumerate(plant_names, 1):
        print(f"{i}. {name}")

    while True:
        if plant_choice == "":
            title = "Відвідано"
            break
        try:
            plant_choice = int(input("Введи номер рослини: "))
            title = plant_names[plant_choice - 1]
            break
        except (ValueError, IndexError):
            print("Неправильний вибір. Ще разок.")

    plant_color = plants.get(title, {}).get("color", "#000000")

    return {
        "lat": lat,
        "lng": lng,
        "title": title,
        "description": f"Додано: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        "shape": "default",
        "icon": "plants",
        "color": plant_color,
    }


def remove_duplicates(data):
    unique = []
    seen = set()
    for item in data:
        key = (item["lat"], item["lng"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def sort_data(data, plants):
    plant_order = list(plants.keys())
    data.sort(key=lambda x: (plant_order.index(x["title"]) if x["title"] in plant_order else len(plant_order)))
    return data


def update_and_save_data(data, plants):
    data = remove_duplicates(data)
    data = sort_data(data, plants)
    save_data(data)
    return data


def main():
    plants = load_plants()
    data = load_data()
    session_file = create_session_file()
    session_data = []

    while True:
        new_entry = get_new_entry(plants)

        # знайти дублікат
        duplicate_index = next(
            (i for i, item in enumerate(data) if item["lat"] == new_entry["lat"] and item["lng"] == new_entry["lng"]),
            None,
        )

        if duplicate_index is not None:
            print(f"\nТака точка вже існує: {data[duplicate_index]['title']} ({new_entry['lat']}, {new_entry['lng']})")
            action = input("Enter – перезаписати, напиши 'del' – видалити, все інше – пропустити: ").strip().lower()
            if action == "":
                data[duplicate_index] = new_entry
                session_data = [
                    item for item in session_data if (item["lat"], item["lng"]) != (new_entry["lat"], new_entry["lng"])
                ]  # відкидується співпадаючий запис
                session_data.append(new_entry)  # додається новий
                print("Запис перезаписано")
            elif action == "del":  # elif це наступний крок
                removed_item = data.pop(duplicate_index)
                session_data = [
                    item
                    for item in session_data
                    if (item["lat"], item["lng"]) != (removed_item["lat"], removed_item["lng"])
                ]
                print(f"Запис видалено: {removed_item['title']} ({removed_item['lat']}, {removed_item['lng']})")
            else:
                print("Запис залишено без змін")
                continue  # перехід до наступного введення
        else:
            data.append(new_entry)
            session_data.append(new_entry)
            print(f"\nДодано: ({new_entry['lat']}, {new_entry['lng']})")

        data = update_and_save_data(data, plants)
        update_session_file(session_file, session_data)  # синхронізуємо сесію
        print(f"Файл {json_file}, {txt_file} та файл сесії {session_file} оновлено")


if __name__ == "__main__":
    main()
