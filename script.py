import re
import json
import os

json_file = "dusty_plants.json"
txt_file = "dusty_plants.txt"
plants_file = "plants.json"


def load_plants():
    if not os.path.exists(plants_file):
        raise FileNotFoundError(f"{plants_file} не знайдено!")
    with open(plants_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_data():
    if not os.path.exists(json_file):
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(txt_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def sync_plant_info(data, plants):
    updated = False
    for item in data:
        title = item["title"]
        if title in plants:
            plant_info = plants[title]
            if item.get("description") != plant_info["description"] or item.get("color") != plant_info["color"]:
                item["description"] = plant_info["description"]
                item["color"] = plant_info["color"]
                updated = True
    return data, updated


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

    print("\nОберіть рослину:")
    for i, name in enumerate(plant_names, 1):
        print(f"{i}. {name}")

    while True:
        try:
            plant_choice = int(input("Введи номер рослини: "))
            title = plant_names[plant_choice - 1]
            break
        except (ValueError, IndexError):
            print("Неправильний вибір. Спробуйте ще раз.")

    plant = plants[title]

    return {
        "lat": lat,
        "lng": lng,
        "title": title,
        "description": plant["description"],
        "shape": "default",
        "icon": "plants",
        "color": plant["color"],
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


def main():
    plants = load_plants()
    data = load_data()

    # Синхронізація описів та кольорів
    data, updated = sync_plant_info(data, plants)
    if updated:
        save_data(data)
        print(f"Файл {json_file} оновлено: виправлені описи та кольори рослин.")

    while True:
        new_entry = get_new_entry(plants)

        # Перевірка на дублікат
        duplicate_index = next(
            (i for i, item in enumerate(data) if item["lat"] == new_entry["lat"] and item["lng"] == new_entry["lng"]),
            None,
        )

        if duplicate_index is not None:
            print(f"\nТака точка вже існує: {data[duplicate_index]['title']} ({new_entry['lat']}, {new_entry['lng']})")
            action = (
                input("Enter – перезаписати, напиши 'del' – видалити, будь-який інший текст – пропустити: ")
                .strip()
                .lower()
            )
            if action == "":
                data[duplicate_index] = new_entry
                print("Запис перезаписано")
            elif action == "del":
                removed_item = data.pop(duplicate_index)
                print(f"Запис видалено: {removed_item['title']} ({removed_item['lat']}, {removed_item['lng']})")
                continue
            else:
                print("Запис залишено без змін")
                continue
        else:
            data.append(new_entry)

        data = remove_duplicates(data)
        data = sort_data(data, plants)
        save_data(data)

        print(f"\nДодано: ({new_entry['lat']}, {new_entry['lng']})")
        print(f"Файл {txt_file} оновлено, як копію JSON для мапи.")


if __name__ == "__main__":
    main()
