from abc import ABC, abstractmethod

class Champion(ABC):
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int):
        self.champion_id = champion_id
        self.name = name
        self.base_hp = base_hp if base_hp > 0 else 100
        self.base_atk = base_atk if base_atk > 0 else 100

    @abstractmethod
    def calculate_skill_damage(self) -> float:
        pass

    def get_combat_power(self) -> float:
        return self.base_hp + (self.calculate_skill_damage() * 1.5)

    def __add__(self, other):
        match other:
            case Champion():
                return self.get_combat_power() + other.get_combat_power()
            case int() | float():
                return self.get_combat_power() + other
            case _:
                return NotImplemented

    def __radd__(self, other):
        match other:
            case 0:
                return self.get_combat_power()
            case int() | float():
                return other + self.get_combat_power()
            case _:
                return NotImplemented

    def __gt__(self, other):
        match other:
            case Champion():
                return self.get_combat_power() > other.get_combat_power()
            case _:
                return NotImplemented


class Warrior(Champion):
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, shield_bonus: int):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.shield_bonus = shield_bonus if shield_bonus >= 0 else 0

    def calculate_skill_damage(self) -> float:
        return self.base_atk * 2 + self.shield_bonus


class Mage(Champion):
    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, ability_power: float):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.ability_power = ability_power if ability_power > 0 else 1.0

    def calculate_skill_damage(self) -> float:
        return self.base_atk * self.ability_power


def show_pool(champion_pool):
    print("\n--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---")
    print(f"{'Mã':<8} | {'Tên tướng':<18} | {'Hệ':<8} | {'HP':<5} | {'ATK':<5} | {'Chỉ số riêng':<15} | {'Chiến lực'}")
    print("-" * 85)
    for c in champion_pool.values():
        match c:
            case Warrior(shield_bonus=armor):
                system_role = "Warrior"
                special_stat = f"Armor: {armor}"
            case Mage(ability_power=ap):
                system_role = "Mage"
                special_stat = f"AP: {ap}"
            case _:
                system_role = "Unknown"
                special_stat = "None"
            
        print(f"{c.champion_id:<8} | {c.name:<18} | {system_role:<8} | {c.base_hp:<5} | {c.base_atk:<5} | {special_stat:<15} | {c.get_combat_power():.0f}")
    print("-" * 85)


def add_champion(champion_pool):
    print("\n--- TẠO TƯỚNG MỚI ---")
    print("1. Hệ Warrior (Chiến binh)")
    print("2. Hệ Mage (Pháp sư)")
    choice = input("Chọn hệ tướng (1-2): ").strip()
    
    match choice:
        case '1' | '2':
            pass
        case _:
            print("Lựa chọn hệ tướng không hợp lệ!")
            return

    c_id = input("Nhập mã tướng: ").strip().upper()
    if c_id in champion_pool:
        print(f"Lỗi: Mã tướng [{c_id}] đã tồn tại trong bể tướng!")
        return

    name = input("Nhập tên tướng: ").strip()
    
    try:
        hp = int(input("Nhập HP: "))
        atk = int(input("Nhập ATK: "))
        
        match choice:
            case '1':
                armor = int(input("Nhập Armor (Giáp): "))
                new_champ = Warrior(c_id, name, hp, atk, armor)
                champion_pool[c_id] = new_champ
                print(f"\nThêm tướng Warrior thành công!")
            case '2':
                ap = float(input("Nhập Hệ số phép thuật (AP): "))
                new_champ = Mage(c_id, name, hp, atk, ap)
                champion_pool[c_id] = new_champ
                print(f"\nThêm tướng Mage thành công!")
            
        print(f"Mã: {new_champ.champion_id} | Tên: {new_champ.name} | Chiến lực: {new_champ.get_combat_power():.0f}")
        
    except ValueError:
        print("Lỗi: Vui lòng nhập đúng định dạng số cho các chỉ số!")


def compare_champions(champion_pool):
    print("\n--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---")
    id1 = input("Nhập mã tướng thứ nhất: ").strip().upper()
    id2 = input("Nhập mã tướng thứ hai: ").strip().upper()

    if id1 not in champion_pool:
        print(f"Mã tướng [{id1}] không hợp lệ, bỏ qua!")
        return
    if id2 not in champion_pool:
        print(f"Mã tướng [{id2}] không hợp lệ, bỏ qua!")
        return

    c1 = champion_pool[id1]
    c2 = champion_pool[id2]

    role1 = "Warrior" if isinstance(c1, Warrior) else "Mage"
    role2 = "Warrior" if isinstance(c2, Warrior) else "Mage"

    print("\nThông tin so sánh:")
    print(f"{c1.champion_id} - {c1.name} | Hệ: {role1} | Chiến lực: {c1.get_combat_power():.0f}")
    print(f"{c2.champion_id} - {c2.name} | Hệ: {role2} | Chiến lực: {c2.get_combat_power():.0f}")

    if c1 > c2:
        print(f"Kết quả: {c1.champion_id} - {c1.name} mạnh hơn {c2.champion_id} - {c2.name}.")
    elif c2 > c1:
        print(f"Kết quả: {c2.champion_id} - {c2.name} mạnh hơn {c1.champion_id} - {c1.name}.")
    else:
        print("Kết quả: Hai quân cờ có sức mạnh ngang nhau.")


def calculate_team_power(champion_pool):
    print("\n--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---")
    raw_input = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: ")
    input_ids = [i.strip().upper() for i in raw_input.split(",") if i.strip()]
    
    team_list = []
    for c_id in input_ids:
        if c_id in champion_pool:
            team_list.append(champion_pool[c_id])
        else:
            print(f"Mã tướng [{c_id}] không hợp lệ, bỏ qua!")

    if not team_list:
        print("Đội hình trống hoặc không có tướng nào hợp lệ.")
        return

    print("\nDanh sách đội hình:")
    for idx, c in enumerate(team_list, 1):
        print(f"{idx}. {c.champion_id} - {c.name} | Chiến lực: {c.get_combat_power():.0f}")

    total_power = sum(team_list)
    print(f"Tổng chiến lực đội hình: {total_power:.0f}")


def main():
    champion_pool = {
        "WAR01": Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
        "WAR02": Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
        "MAG01": Mage("MAG01", "Rikkei Wizard", 800, 500, 1.5)
    }

    while True:
        print("\n================ RIKKEI RPG MANAGER ================")
        print("1. Hiển thị bể tướng hiện có")
        print("2. Thêm quân cờ mới")
        print("3. So sánh 2 quân cờ")
        print("4. Tính tổng chiến lực Đội Hình Ra Sân")
        print("5. Thoát chương trình")
        
        choice = input("Chọn chức năng (1-5): ").strip()
        
        match choice:
            case '1':
                show_pool(champion_pool)
            case '2':
                add_champion(champion_pool)
            case '3':
                compare_champions(champion_pool)
            case '4':
                calculate_team_power(champion_pool)
            case '5':
                print("Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
                break
            case _:
                print("Chức năng không hợp lệ, vui lòng chọn lại từ 1 đến 5.")

if __name__ == "__main__":
    main()