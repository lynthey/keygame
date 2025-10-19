import time
import json
import os
import random
import string
import sys

SAVE_DATA = "scores.json"


def load_scores():
    if not os.path.exists(SAVE_DATA):
        return []
    f = open(SAVE_DATA, "r", encoding="utf-8")
    return json.load(f)

def save_score(name, newscore):
    scores = load_scores()
    scores.append({"name": name, "score": newscore})
    scores = sorted(scores, key=lambda x: x["score"])[:10]
    f = open(SAVE_DATA, "w", encoding="utf-8")
    json.dump(scores, f, ensure_ascii=False, indent=2)

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")

def show_title():
    clear_screen()
    print("=-" * 22)
    print("           TIME ATACK A to Z")
    print("=-" * 22)
    scores = load_scores()
    print("\nTOP 3 SCORES:")
    for i, s in enumerate(scores, start=1):
        print(f" {i}. {s['name']} - {s['score']:.2f} 秒")
    print("\n")


def countdown():
    print("Ready?", end="", flush=True)
    for i in range(3, 0, -1):
        print(f" {i}", end="", flush=True)
        time.sleep(1)
    print(" GO!\n")
    time.sleep(0.3)

def getch_unix():
    import tty, termios
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def getch_win():
    import msvcrt
    return msvcrt.getch().decode()

def getch():
    func = getch_win if sys.platform == "win32" else getch_unix
    return func()

def play_game():
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    input("\n <PUT ENTER TO START>")
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
    show_title()
    name = input("YOUR NAME? ").strip().upper() or "PLAYER"
    print("\n")
    while True:
      score = play_game()
      print(f"\n GREAT JOB {name}! YOUR TIME IS {score:.2f} sec!")
      save_score(name, score)
      input("\n <PUSH ENTER TO START>")
      show_title()

if __name__ == "__main__":
    main()
