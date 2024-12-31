import time
import sys
import random
from datetime import datetime
import threading
import winsound
from tqdm import tqdm
from art import text2art
from termcolor import colored
from colorama import Fore, Style
from itertools import cycle

# ==== Global Variables ====
TARGET_YEAR = 2025


# ==== Utility Functions ====
def typewriter_effect(text, delay=0.1):
    """
    Displays text character by character with a typewriter effect.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def play_sound(file_name, async_mode=False):
    """
    Plays the specified sound file.
    """
    mode = winsound.SND_FILENAME | (winsound.SND_ASYNC if async_mode else 0)
    winsound.PlaySound(file_name, mode)


def stop_all_sounds():
    """
    Stops all currently playing sounds.
    """
    winsound.PlaySound(None, winsound.SND_PURGE)


# ==== Animation and Effects ====
def countdown_with_progress_bar(seconds, message="Geri sayım"):
    """
    Displays a countdown timer with a progress bar, enhanced with a New Year theme.
    """
    snowflakes = cycle(["❄️", "⛄", "✨", "🎄"])
    desc = f"{Fore.CYAN}⌛ {message} 🎅{Style.RESET_ALL}"
    with tqdm(
        total=seconds,
        desc=desc,
        bar_format='{desc} |{bar}| {postfix}',
        ncols=75,
        ascii=" ░▒▓█"
    ) as pbar:
        for remaining in range(seconds, 0, -1):
            icon = next(snowflakes)
            pbar.set_postfix_str(
                f'{remaining // 60:02d}:{remaining % 60:02d} qaldı {icon}')
            pbar.update(1)
            time.sleep(1)
        pbar.set_postfix_str(f'00:00 qaldı 🎆')
        pbar.refresh()


def fireworks_effect(iterations=25, min_icons=10, max_icons=35, delay=0.3):
    """
    Displays a fireworks animation with 5 lines of colorful icons and clears them after each iteration.
    """

    fireworks = [
        "🎆", "🎇", "💥", "🌟", "✨",
        "💫", "🌠", "🎉", "🎊", "🧨",
        "🎈", "🎁", "🤩", "🥳", "🔔",
        "🎀", "🍾", "🥂", "🍷", "🍭",
        "🍬", "❄️", "⛄", "🎄", "🎟️",
        "🎶", "🎯", "🪐", "🌕", "🌓"
    ]

    colors = ["red", "yellow", "green", "cyan", "magenta", "blue", "white"]
    attrs = ["bold", "blink", "underline"]

    for _ in range(iterations):
        lines = []
        for _ in range(5):  # Number of lines to display
            line = " ".join([
                colored(random.choice(fireworks),
                        random.choice(colors),
                        attrs=[random.choice(attrs)])
                for _ in range(random.randint(min_icons, max_icons))
            ])
            lines.append(line)
            print(line)

        # Wait a moment to let the effect be visible
        time.sleep(delay)

        sys.stdout.write("\033[F" * len(lines))
        for _ in range(len(lines)):
            sys.stdout.write("\033[K")
        sys.stdout.flush()


# ==== Art and Messages ====
def display_intro_message():
    """
    Displays the introduction message.
    """
    border = "✨" * 40
    empty_line = f"✨{' ' * 76}✨"

    content = "✨{: ^76}✨".format(f"Son Saniyələr: {TARGET_YEAR}-ə Doğru")

    print(f"\n{border}")
    print(empty_line)
    print(content)
    print(empty_line)
    print(f"{border}\n")


def display_exit_message():
    """
    Displays the exit message.
    """
    print("\n" + "✨" * 40 + "\n")


def display_gradient_text(text, font="big"):
    """
    Displays ASCII art with gradient colors.
    """
    art_message = text2art(text, font=font)
    colors = [
        Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX,
        Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.LIGHTCYAN_EX,
        Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX
    ]
    color_cycle = cycle(colors)

    gradient_art = ""
    for char in art_message:
        gradient_art += f"{next(color_cycle)}{char}{Style.RESET_ALL}" if char.strip() else char

    print(gradient_art)


def display_new_year_message():
    """
    Displays the New Year greeting message.
    """
    display_gradient_text("HAPPY   NEW   YEAR!")
    messages = [
        ("🎄 YENİ İLİNİZ MÜBARƏK! 🎄", "red"),
        (f"🌟 {TARGET_YEAR} sevgi, həvəs və uğurla dolu, xəyallarınızı gerçəyə çevirən bir il olsun! 🌟", "blue"),
        ("🎇 Hər addımınız sizi böyük nailiyyətlərə və yeni zirvələrə aparsın! 🎇", "green"),
        ("✨ Sizə sağlamlıq, sevinc və tükənməz enerji ilə dolu, xoş xatirələr yaradacağınız bir il arzulayıram! ✨", "magenta"),
        ("\n💻  Happy Coding! 💻", "yellow")
    ]
    for message, color in messages:
        typewriter_effect(colored(message, color, attrs=["bold"]), delay=0.1)


# ==== Main Program ====
def main():
    """
    Entry point for the New Year Countdown program.
    """
    display_intro_message()

    # Countdown
    now = datetime.now()
    target = datetime(year=TARGET_YEAR, month=1, day=1,
                      hour=0, minute=0, second=0)
    seconds_to_target = int((target - now).total_seconds())
    countdown_with_progress_bar(
        max(10, seconds_to_target), f"{TARGET_YEAR} üçün geri sayım")
    print("\n")

    # Fireworks animation and sound
    firework_sound_thread = threading.Thread(
        target=lambda: play_sound("assets/sounds/celebration_fireworks.wav"))
    firework_sound_thread.start()
    fireworks_effect()
    firework_sound_thread.join()

    # Background music
    music_thread = threading.Thread(target=lambda: play_sound(
        "assets/sounds/happy_new_year.wav", async_mode=True))
    music_thread.start()

    # Display New Year message
    display_new_year_message()

    # Stop all sounds
    stop_all_sounds()

    display_exit_message()


if __name__ == "__main__":
    main()
