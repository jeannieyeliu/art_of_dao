import random
import os
import json
from datetime import datetime

# [The existing TAROT_SPREADS and CARD_DESCRIPTIONS dictionaries remain unchanged]

class TarotCLI:
    def __init__(self):
        self.cards_folder = "TarotCards"
        self.readings_file = "tarot_readings.json"

    def run(self):
        while True:
            self.print_header("欢迎使用塔罗牌阵应用")
            print("1. 进行新的塔罗牌阵")
            print("2. 查看保存的塔罗牌阵")
            print("3. 查看牌阵释义")
            print("4. 搜索保存的塔罗牌阵")
            print("5. 退出")
            
            choice = input("请选择操作 (1/2/3/4/5): ")
            
            if choice == "1":
                self.new_reading()
            elif choice == "2":
                self.view_saved_readings()
            elif choice == "3":
                self.view_spread_meanings()
            elif choice == "4":
                self.search_readings()
            elif choice == "5":
                print("谢谢使用，再见！")
                break
            else:
                print("无效的选择，请重试。")

    def new_reading(self):
        self.print_header("新的塔罗牌阵")
        question = input("找一个安静的环境，输入你的问题，问题尽量具体、清晰：\n")
        
        self.print_header("选择牌阵")
        for i, spread in enumerate(TAROT_SPREADS, 1):
            print(f"{i}. {spread['name']} - {spread['description']} ({spread['cards']}张牌)")
            print(f"   {spread['feature']}")
        
        selected_spread = self.get_valid_spread_choice()
        
        self.print_header(f"你选择了 {selected_spread['name']}")
        print("牌阵位置释义：")
        for i, position in enumerate(selected_spread['positions'], 1):
            print(f"{i}. {position}")
        input("\n按回车键抽牌...")
        
        reading = self.draw_cards(selected_spread)
        reading["question"] = question
        reading["spread"] = selected_spread["name"]
        reading["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.save_reading(reading)
        self.save_reading_to_txt(reading)

    def get_valid_spread_choice(self):
        while True:
            try:
                spread_choice = int(input("\n请选择牌阵 (输入数字): ")) - 1
                if 0 <= spread_choice < len(TAROT_SPREADS):
                    return TAROT_SPREADS[spread_choice]
                else:
                    print("无效的选择，请输入1到7之间的数字。")
            except ValueError:
                print("请输入有效的数字。")

    def draw_cards(self, spread):
        all_cards = [f for f in os.listdir(self.cards_folder) if f.endswith('.jpg') and f != "普及版背面.jpg"]
        drawn = random.sample(all_cards, spread['cards'])
        orientations = [random.choice(["正位", "逆位"]) for _ in range(spread['cards'])]
        
        reading = {"cards": []}
        
        self.print_header("抽到的牌")
        for i in range(1, spread['cards'] + 1):
            print(f"{i}. [牌面朝下]")
        
        flipped_cards = set()
        while len(flipped_cards) < len(drawn):
            try:
                card_to_flip = int(input("\n选择要翻开的牌 (输入数字)，或输入0退出: "))
                if card_to_flip == 0:
                    break
                if 1 <= card_to_flip <= len(drawn):
                    if card_to_flip in flipped_cards:
                        print("这张牌已经翻开了，请选择其他牌。")
                    else:
                        flipped_cards.add(card_to_flip)
                        self.print_header(f"第 {card_to_flip} 张牌")
                        card = drawn[card_to_flip-1]
                        orientation = orientations[card_to_flip-1]
                        meaning = CARD_DESCRIPTIONS.get(card, '未知')
                        position = spread['positions'][card_to_flip-1]
                        print(f"翻开的牌: {card} ({orientation})")
                        print(f"含义: {meaning}")
                        print(f"位置: {position}")
                        if orientation == "逆位":
                            print("注意：这是逆位牌，可能表示该牌的能量受阻或相反。")
                        
                        reading["cards"].append({
                            "name": card,
                            "orientation": orientation,
                            "meaning": meaning,
                            "position": position
                        })
                else:
                    print("无效的选择，请重试。")
            except ValueError:
                print("请输入有效的数字。")
        
        return reading

    def save_reading(self, reading):
        try:
            if os.path.exists(self.readings_file):
                with open(self.readings_file, 'r', encoding='utf-8') as f:
                    readings = json.load(f)
            else:
                readings = []
            
            readings.append(reading)
            
            with open(self.readings_file, 'w', encoding='utf-8') as f:
                json.dump(readings, f, ensure_ascii=False, indent=2)
            
            print("塔罗牌阵已保存。")
        except Exception as e:
            print(f"保存塔罗牌阵时出错: {e}")

    def save_reading_to_txt(self, reading):
        filename = f"tarot_reading_{reading['datetime'].replace(':', '-')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"日期: {reading['datetime']}\n")
            f.write(f"问题: {reading['question']}\n")
            f.write(f"牌阵: {reading['spread']}\n\n")
            f.write("实践过程：\n")
            for i, card in enumerate(reading['cards'], 1):
                f.write(f"第 {i} 张牌:\n")
                f.write(f"名称: {card['name']}\n")
                f.write(f"方向: {card['orientation']}\n")
                f.write(f"含义: {card['meaning']}\n")
                f.write(f"位置: {card['position']}\n")
                if card['orientation'] == "逆位":
                    f.write("注意：这是逆位牌，可能表示该牌的能量受阻或相反。\n")
                f.write("\n")
            f.write("\n结果解读：\n")
            f.write("（这里可以添加对整体牌阵的解读，目前留空供用户自行填写）\n")
        print(f"塔罗牌阵结果已自动保存到文件: {filename}")

    def view_saved_readings(self):
        if not os.path.exists(self.readings_file):
            print("没有保存的塔罗牌阵。")
            return
        
        try:
            with open(self.readings_file, 'r', encoding='utf-8') as f:
                readings = json.load(f)
            
            if not readings:
                print("没有保存的塔罗牌阵。")
                return
            
            self.print_header("保存的塔罗牌阵")
            for i, reading in enumerate(readings, 1):
                print(f"{i}. 日期: {reading['datetime']}")
                print(f"   问题: {reading['question']}")
                print(f"   牌阵: {reading['spread']}")
                print()
            
            choice = int(input("选择要查看的塔罗牌阵 (输入数字)，或输入0返回: "))
            if 1 <= choice <= len(readings):
                self.display_reading(readings[choice-1])
            elif choice != 0:
                print("无效的选择。")
        except Exception as e:
            print(f"查看保存的塔罗牌阵时出错: {e}")

    def display_reading(self, reading):
        self.print_header(f"塔罗牌阵 - {reading['datetime']}")
        print(f"问题: {reading['question']}")
        print(f"牌阵: {reading['spread']}")
        print()
        for i, card in enumerate(reading['cards'], 1):
            print(f"第 {i} 张牌:")
            print(f"名称: {card['name']}")
            print(f"方向: {card['orientation']}")
            print(f"含义: {card['meaning']}")
            print(f"位置: {card['position']}")
            if card['orientation'] == "逆位":
                print("注意：这是逆位牌，可能表示该牌的能量受阻或相反。")
            print()

    def view_spread_meanings(self):
        self.print_header("牌阵释义")
        for i, spread in enumerate(TAROT_SPREADS, 1):
            print(f"{i}. {spread['name']}")
            print(f"   描述: {spread['description']}")
            print(f"   特点: {spread['feature']}")
            print("   位置释义:")
            for j, position in enumerate(spread['positions'], 1):
                print(f"      {j}. {position}")
            print()
        
        input("按回车键返回主菜单...")

    def search_readings(self):
        if not os.path.exists(self.readings_file):
            print("没有保存的塔罗牌阵。")
            return
        
        try:
            with open(self.readings_file, 'r', encoding='utf-8') as f:
                readings = json.load(f)
            
            if not readings:
                print("没有保存的塔罗牌阵。")
                return
            
            self.print_header("搜索保存的塔罗牌阵")
            search_term = input("请输入搜索关键词（日期或问题内容）：").lower()
            
            matched_readings = []
            for reading in readings:
                if search_term in reading['datetime'].lower() or search_term in reading['question'].lower():
                    matched_readings.append(reading)
            
            if not matched_readings:
                print("未找到匹配的塔罗牌阵。")
                return
            
            print(f"找到 {len(matched_readings)} 个匹配的塔罗牌阵：")
            for i, reading in enumerate(matched_readings, 1):
                print(f"{i}. 日期: {reading['datetime']}")
                print(f"   问题: {reading['question']}")
                print(f"   牌阵: {reading['spread']}")
                print()
            
            choice = int(input("选择要查看的塔罗牌阵 (输入数字)，或输入0返回: "))
            if 1 <= choice <= len(matched_readings):
                self.display_reading(matched_readings[choice-1])
            elif choice != 0:
                print("无效的选择。")
        except Exception as e:
            print(f"搜索保存的塔罗牌阵时出错: {e}")

    def print_header(self, text):
        print("\n" + "=" * 50)
        print(text.center(50))
        print("=" * 50 + "\n")

if __name__ == "__main__":
    app = TarotCLI()
    app.run()
