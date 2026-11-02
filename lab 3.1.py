import json
import random
import os


# ---------- ЗАДАНИЕ 1. СПРАВОЧНИКИ ----------

heroes = {
    "Мурзик": {
        "вид": "кот-рыцарь",
        "сила": 2,
        "hp": 20,
        "золото": 5
    },
    "Жужа": {
        "вид": "сколопендра-бард",
        "сила": 1,
        "hp": 15,
        "золото": 8
    },
    "Перо": {
        "вид": "голубь-маг",
        "сила": 3,
        "hp": 12,
        "золото": 3
    }
}

shop = [
    {"name": "Сарделька", "price": 10, "heal": 5},
    {"name": "Молоко", "price": 8, "heal": 3},
    {"name": "Когтеточка +5", "price": 25, "power": 2}
]


# ---------- ЗАДАНИЕ 2. БРОСОК КУБИКА ----------

def roll_dice(sides=6):
    return random.randint(1, sides)


# ---------- ЗАДАНИЕ 3. КЛАСС ПЕРСОНАЖА ----------

class Character:
    def __init__(self, name, view, power, hp, gold):
        self.name = name
        self.view = view
        self.power = power
        self.hp = hp
        self.max_hp = hp
        self.gold = gold
        self.inventory = []

    def info(self):
        return (
            f"Имя: {self.name}\n"
            f"Вид: {self.view}\n"
            f"Сила: {self.power}\n"
            f"Здоровье: {self.hp}/{self.max_hp}\n"
            f"Золото: {self.gold}"
        )

    def heal(self, amount):
        old_hp = self.hp
        self.hp = min(self.hp + amount, self.max_hp)
        return self.hp - old_hp

    def take_damage(self, dmg):
        self.hp = max(0, self.hp - dmg)

    def add_item(self, item_name):
        self.inventory.append(item_name)

    def show_items(self):
        if not self.inventory:
            print("Инвентарь пуст.")
            return

        print("Инвентарь героя:")

        for index, item in enumerate(self.inventory, start=1):
            print(f"{index}. {item}")


# ---------- ЗАДАНИЕ 4. СОЗДАНИЕ ГЕРОЯ ----------

def create_hero():
    print("\n===== СОЗДАНИЕ ГЕРОЯ =====")

    names = list(heroes.keys())

    for index, name in enumerate(names, start=1):
        data = heroes[name]
        print(
            f"{index}. {name} | {data['вид']} | "
            f"Сила: {data['сила']} | HP: {data['hp']} | "
            f"Золото: {data['золото']}"
        )

    while True:
        choice = input("Выбери героя (1-3): ").strip()

        if choice in ("1", "2", "3"):
            name = names[int(choice) - 1]
            break

        print("Введи число от 1 до 3.")

    roles = {
        "рыцарь": 4,
        "маг": 3,
        "вор": 2
    }

    print("\nВыбери класс:")

    for role in roles:
        print(f"- {role}")

    while True:
        role = input("Твой класс: ").strip().lower()

        if role in roles:
            break

        print("Такого класса нет.")

    data = heroes[name]

    hero = Character(
        name,
        data["вид"],
        data["сила"] + roles[role],
        data["hp"] + roles[role],
        data["золото"]
    )

    print("\nГерой создан!")
    print(hero.info())

    return hero


# ---------- ЗАДАНИЕ 5. КЛАСС БОССА ----------

class Boss(Character):
    def take_damage(self, dmg):
        reduced_damage = max(1, dmg // 2)
        super().take_damage(reduced_damage)


# ---------- ЗАДАНИЕ 6. БОЙ И КРАЖА ----------

def steal(victim):
    stolen = min(roll_dice(5), victim.gold)
    victim.gold -= stolen
    return stolen


def battle(hero, enemy):
    print("\n===== НАЧАЛО БОЯ =====")
    print(f"{hero.name} против {enemy.name}")

    if hero.hp <= 0:
        print("Герой не может сражаться без здоровья.")
        return False

    if hero.name == "Жужа":
        stolen = steal(enemy)
        hero.gold += stolen
        print(f"Жужа украла {stolen} золота.")

    while hero.hp > 0 and enemy.hp > 0:
        input("\nНажми Enter, чтобы атаковать...")

        damage = hero.power + roll_dice()
        enemy.take_damage(damage)

        print(f"{hero.name} наносит {damage} урона.")
        print(f"Здоровье противника: {enemy.hp}/{enemy.max_hp}")

        if enemy.hp <= 0:
            print(f"\nПобеда! Противник {enemy.name} побеждён.")
            hero.gold += enemy.gold
            print(f"Получено золота: {enemy.gold}")
            print(f"Всего золота: {hero.gold}")
            return True

        damage = enemy.power + roll_dice()
        hero.take_damage(damage)

        print(f"{enemy.name} наносит {damage} урона.")
        print(f"Твоё здоровье: {hero.hp}/{hero.max_hp}")

        if hero.hp <= 0:
            print("\nГерой потерпел поражение.")
            return False

    return hero.hp > 0


# ---------- ЗАДАНИЕ 7. ЛАВКА ПРИЮТА ----------

def buy_item(hero):
    print("\n===== ЛАВКА ПРИЮТА =====")
    print(f"Твоё золото: {hero.gold}")

    for index, item in enumerate(shop, start=1):
        print(f"{index}. {item['name']} — {item['price']} золота")

    print("0. Вернуться в меню")

    choice = input("Выбери товар: ").strip()

    if choice == "0":
        print("Возвращаемся в меню.")
        return

    if choice not in ("1", "2", "3"):
        print("Неверный номер товара.")
        return

    item = shop[int(choice) - 1]

    if hero.gold < item["price"]:
        print("Недостаточно золота.")
        return

    hero.gold -= item["price"]

    if "heal" in item:
        healed = hero.heal(item["heal"])
        print(f"Восстановлено здоровья: {healed} HP.")

    if "power" in item:
        hero.power += item["power"]
        print(f"Сила увеличена на {item['power']}.")

    hero.add_item(item["name"])

    print(f"Куплено: {item['name']}.")
    print(f"Осталось золота: {hero.gold}")


# ---------- ЗАДАНИЕ 8. СВОДКА ПО ПРИЮТУ ----------

def report():
    print("\n===== СВОДКА ПО ПРИЮТУ =====")
    print(f"{'Имя':<12}{'Сила':<10}{'Золото':<10}{'HP':<10}")

    total_power = 0

    for name, data in heroes.items():
        print(
            f"{name:<12}"
            f"{data['сила']:<10}"
            f"{data['золото']:<10}"
            f"{data['hp']:<10}"
        )

        total_power += data["сила"]

    average_power = total_power / len(heroes)

    print(f"\nКоличество героев: {len(heroes)}")
    print(f"Средняя сила: {average_power:.1f}")


# ---------- ЗАДАНИЕ 9. СОХРАНЕНИЕ И ЗАГРУЗКА ----------

SAVE_FILE = "save.json"


def save_game(hero):
    data = {
        "name": hero.name,
        "view": hero.view,
        "power": hero.power,
        "hp": hero.hp,
        "max_hp": hero.max_hp,
        "gold": hero.gold,
        "inventory": hero.inventory
    }

    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Игра успешно сохранена.")

    except OSError as error:
        print(f"Не удалось сохранить игру: {error}")


def load_game():
    if not os.path.exists(SAVE_FILE):
        return None

    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        hero = Character(
            data["name"],
            data["view"],
            data["power"],
            data["max_hp"],
            data["gold"]
        )

        hero.hp = max(0, min(data["hp"], hero.max_hp))
        hero.inventory = data.get("inventory", [])

        print(f"Сохранение загружено: {hero.name}")

        return hero

    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Не удалось загрузить сохранение: {error}")
        return None


# ---------- ЗАДАНИЕ 10. ОБРАБОТКА МЕНЮ ----------

def menu_loop(hero):
    actions = {
        "1": show_character,
        "2": enter_dungeon,
        "3": buy_item,
        "4": fight_boss,
        "5": show_inventory,
        "6": show_report,
        "7": heal_character
    }

    while True:
        print("\n" + "=" * 40)
        print("ГИЛЬДИЯ КОТОВ-ПРИКЛЮЧЕНЦЕВ")
        print("=" * 40)
        print("1 — Карточка героя")
        print("2 — Подземелье")
        print("3 — Лавка приюта")
        print("4 — Бой с боссом")
        print("5 — Инвентарь")
        print("6 — Сводка по приюту")
        print("7 — Лечение")
        print("8 — Сохранить игру")
        print("0 — Выход")
        print("=" * 40)

        try:
            choice = input("Твой выбор: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nЗавершение игры.")
            save_game(hero)
            break

        print(f"\nОбработка выбора: {choice}")

        if choice == "0":
            save_game(hero)
            print("До встречи!")
            break

        if choice == "8":
            save_game(hero)
            continue

        action = actions.get(choice)

        if action is None:
            print("Неверный пункт меню. Введи число от 0 до 8.")
            continue

        try:
            action(hero)
        except Exception as error:
            print(f"Ошибка при выполнении пункта {choice}: {error}")

        input("\nНажми Enter, чтобы вернуться в меню...")


# ---------- ЗАДАНИЕ 11. ФУНКЦИИ МЕНЮ ----------

def show_character(hero):
    print("\n===== КАРТОЧКА ГЕРОЯ =====")
    print(hero.info())


def enter_dungeon(hero):
    print("\n===== ПОДЗЕМЕЛЬЕ =====")

    if hero.hp <= 0:
        print("У героя нет здоровья. Сначала вылечись.")
        return

    enemy = Character(
        "Пыльный голем",
        "голем",
        4,
        20,
        12
    )

    battle(hero, enemy)


def fight_boss(hero):
    print("\n===== БОЙ С БОССОМ =====")

    if hero.hp <= 0:
        print("У героя нет здоровья. Сначала вылечись.")
        return

    boss = Boss(
        "Сколопендриха-матриарх",
        "босс",
        6,
        30,
        30
    )

    battle(hero, boss)


def show_inventory(hero):
    print("\n===== ИНВЕНТАРЬ =====")
    hero.show_items()


def show_report(hero):
    report()


def heal_character(hero):
    print("\n===== ЛЕЧЕНИЕ =====")

    if hero.hp <= 0:
        print("Герой восстанавливается после поражения.")

    healed = hero.heal(5)

    print(f"Восстановлено здоровья: {healed} HP.")
    print(hero.info())


# ---------- ЗАДАНИЕ 12. ЗАПУСК ПРОГРАММЫ ----------

def main():
    print("Запуск игры «Гильдия котов-приключенцев»")

    hero = load_game()

    if hero is None:
        print("\nСохранение не найдено. Создаём нового героя.")
        hero = create_hero()

    print("\nИгра готова к запуску.")
    print(hero.info())

    menu_loop(hero)


if __name__ == "__main__":
    main()
