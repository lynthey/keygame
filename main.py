import time
import json
import os
import random
import string
import sys
import termios
import tty

SAVE_FILE = "scores.json"


def load_scores():
    if not os.path.exists(SAVE_FILE):
        return []
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_score(name, score):
    scores = load_scores()
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"])[:10]
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)


def show_title():
    print("=" * 50)
    print("           TYPE RACE - A〜Z SPEED GAME")
    print("=" * 50)
    scores = load_scores()
    print("\nTOP 3 SCORES:")
    for i, s in enumerate(scores[:3], start=1):
        print(f" {i}. {s['name']} - {s['score']:.2f} 秒")
    print("\n")


def countdown():
    print("Ready?", end="", flush=True)
    for i in range(3, 0, -1):
        print(f" {i}", end="", flush=True)
        time.sleep(1)
    print(" GO!\n")
    time.sleep(0.3)


def getch():
    """エンター不要で1文字取得"""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch


def play_game():
    letters = list(string.ascii_uppercase)
    print("A〜Zまで順にタイプしてください！")
    input("Enterキーでスタートします。")
    countdown()
    start = time.time()
    for target in letters:
        while True:
            print(f"{target} >", end=" ", flush=True)
            key = getch().upper()
            print(key)
            if key == target:
                break
    end = time.time()
    return end - start


def main():
    os.system("clear" if os.name == "posix" else "cls")
    show_title()
    name = input("名前を入力してください: ").strip() or "PLAYER"
    print("\n")
    score = play_game()
    print(f"\nタイム: {score:.2f} 秒")
    save_score(name, score)
    print("スコアを保存しました！")
    print("\n--- TOP 3 ---")
    for i, s in enumerate(load_scores()[:3], start=1):
        print(f" {i}. {s['name']} - {s['score']:.2f} 秒")


if __name__ == "__main__":
    main()
