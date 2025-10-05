import tkinter as tk
from tkinter import ttk
import random
from PIL import Image, ImageTk
import os
from datetime import datetime
import re

# Define tarot spreads
TAROT_SPREADS = [
    {
        "name": "圣三角牌阵",
        "description": "事件基本发展脉络",
        "cards": 3,
        "feature": "结构简单，适合快速了解问题的过去、现在与未来趋势"
    },
    {
        "name": "爱情幸福十字牌阵",
        "description": "爱情发展、双方态度",
        "cards": 5,
        "feature": "针对爱情关系进行深入分析，能看清现状、阻碍及未来结果"
    },
    {
        "name": "恋人三角牌阵",
        "description": "恋爱与婚姻问题",
        "cards": 4,
        "feature": "侧重分析恋爱双方的个人状态及彼此的互动关系"
    },
    {
        "name": "塞尔特十字牌阵",
        "description": "综合性复杂问题",
        "cards": 10,
        "feature": "分析全面深入，涵盖问题核心、内在因素、外界环境及最终结果等多个层面"
    },
    {
        "name": "四要素牌阵",
        "description": "寻求问题解决方案",
        "cards": 4,
        "feature": "从行动、沟通、情感、物质四个维度提供具体行动建议"
    },
    {
        "name": "时间之流牌阵",
        "description": "事件随时间推移的变化",
        "cards": 5,  # Using 5 as the maximum
        "feature": "清晰展示事件在时间轴上的发展进程"
    },
    {
        "name": "吉普赛十字牌阵",
        "description": "爱情问题深度剖析",
        "cards": 5,
        "feature": "以十字形展开，逐层揭示双方心态、相处模式及关系结局"
    }
]

class TarotApp:
    def __init__(self, master):
        self.master = master
        self.master.title("塔罗牌阵应用")
        self.master.geometry("800x800")  # Increased height to 800

        self.cards_folder = "TarotCards"
        self.results_folder = "Taro_results"
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)
        
        self.card_back = ImageTk.PhotoImage(Image.open(os.path.join(self.cards_folder, "普及版背面.jpg")).resize((100, 150)))
        self.drawn_cards = []
        self.card_labels = []  # New list to store labels for card names
        self.flipped_cards = 0  # Counter for flipped cards
        self.total_cards = 0  # Total number of cards in the spread

        self.create_widgets()

    def create_widgets(self):
        # Question input
        tk.Label(self.master, text="找一个安静的环境，输入你的问题，问题尽量具体、清晰。").pack(pady=10)
        self.question_entry = tk.Entry(self.master, width=50)
        self.question_entry.pack(pady=5)

        # Tarot spread selection
        tk.Label(self.master, text="选择牌阵:").pack(pady=10)
        self.spread_var = tk.StringVar()
        for spread in TAROT_SPREADS:
            ttk.Radiobutton(self.master, 
                            text=f"{spread['name']} - {spread['description']} ({spread['cards']}张牌)\n{spread['feature']}", 
                            variable=self.spread_var, 
                            value=spread['name']).pack(anchor='w', padx=20, pady=5)

        # Draw cards button
        tk.Button(self.master, text="抽牌", command=self.draw_cards).pack(pady=20)

        # Frame for displaying cards
        self.cards_frame = tk.Frame(self.master)
        self.cards_frame.pack(pady=20)

    def draw_cards(self):
        # Clear previous cards and labels
        for widget in self.cards_frame.winfo_children():
            widget.destroy()
        self.drawn_cards.clear()
        self.card_labels.clear()
        self.flipped_cards = 0  # Reset flipped cards counter

        # Get selected spread
        selected_spread = next((spread for spread in TAROT_SPREADS if spread['name'] == self.spread_var.get()), None)
        if not selected_spread:
            return

        # Draw cards
        all_cards = [f for f in os.listdir(self.cards_folder) if f.endswith('.jpg') and f != "普及版背面.jpg"]
        drawn = random.sample(all_cards, selected_spread['cards'])
        self.total_cards = len(drawn)  # Set total number of cards

        # Display cards face down and create labels
        for i, card in enumerate(drawn):
            is_reversed = random.choice([True, False])  # Randomly decide if the card is reversed
            card_button = tk.Button(self.cards_frame, image=self.card_back, command=lambda x=i, c=card, r=is_reversed: self.flip_card(x, c, r))
            card_button.grid(row=0, column=i, padx=5)
            self.drawn_cards.append((card_button, is_reversed, card))  # Store the card filename as well

            # Create label for card name (initially empty)
            card_label = tk.Label(self.cards_frame, text="")
            card_label.grid(row=1, column=i, padx=5)
            self.card_labels.append(card_label)

    def flip_card(self, index, card, is_reversed):
        # Flip the card to show its face
        card_image = Image.open(os.path.join(self.cards_folder, card)).resize((100, 150))
        if is_reversed:
            card_image = card_image.rotate(180)
        card_image = ImageTk.PhotoImage(card_image)
        self.drawn_cards[index][0].config(image=card_image)
        self.drawn_cards[index][0].image = card_image  # Keep a reference

        # Update the label with the card name (without file extension) and position
        card_name = os.path.splitext(card)[0]
        position = "逆位" if is_reversed else "正位"
        self.card_labels[index].config(text=f"{card_name} ({position})")

        # Increment the flipped cards counter
        self.flipped_cards += 1

        # Check if all cards have been flipped
        if self.flipped_cards == self.total_cards:
            self.save_reading()

    def save_reading(self):
        question = self.question_entry.get()
        current_date = datetime.now().strftime("%Y%m%d")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        spread_name = self.spread_var.get()
        
        # Create a filename-safe version of the question (first 20 characters)
        safe_question = re.sub(r'[^\w\-_\. ]', '_', question[:20])
        filename = f"{current_date}_{safe_question}.txt"
        filepath = os.path.join(self.results_folder, filename)
        
        result = []
        for i, (_, is_reversed, card) in enumerate(self.drawn_cards):
            card_name = os.path.splitext(card)[0]
            position = "逆位" if is_reversed else "正位"
            result.append(f"{card_name} ({position})")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"日期时间: {current_time}\n")
            f.write(f"问题: {question}\n")
            f.write(f"牌阵: {spread_name}\n")
            f.write("结果:\n")
            for i, card_result in enumerate(result, 1):
                f.write(f"  {i}. {card_result}\n")

        print(f"Reading saved to {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TarotApp(root)
    root.mainloop()
