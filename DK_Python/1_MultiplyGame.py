"""Multiply Game

Levels:
 - easy: single-digit x single-digit (1-9)
 - medium: single-digit x double-digit (1-9) x (10-99)
 - hard: double-digit x double-digit (10-99)

On finishing the quiz a 'win' or 'lose' sound plays (Windows) using winsound.Beep.
"""

import random
import platform
import sys
import os
import glob
import urllib.request
import subprocess
import shutil
import pygame


def _wav_files_for(kind: str):
	"""Return list of wav files matching typical names for kind in ./sounds."""
	base = os.path.dirname(__file__)
	snd_dir = os.path.join(base, "sounds")
	if not os.path.isdir(snd_dir):
		return []
	patterns = {
		"win": ["win*.wav", "applause*.wav", "clap*.wav", "cheer*.wav"],
		"lose": ["lose*.wav", "boo*.wav", "buzzer*.wav", "sad*.wav"],
	}
	files = []
	for pat in patterns.get(kind, [f"{kind}*.wav"]):
		files.extend(glob.glob(os.path.join(snd_dir, pat)))
	return files


def _play_wav(filepath: str):
	try:
		import winsound
		winsound.PlaySound(filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
		return True
	except Exception:
		return False


def play_win_sound():
	# Try WAV files first (user can drop WAVs into a 'sounds' folder next to this file)
	wavs = _wav_files_for("win")
	if wavs:
		_play_wav(random.choice(wavs))
		return
	# If no WAVs, try MP3 download & playback, then system messages or beep patterns
	# ensure sounds directory exists
	base = os.path.dirname(__file__)
	snd_dir = os.path.join(base, "sounds")
	os.makedirs(snd_dir, exist_ok=True)
	# default celebration mp3 (royalty-free/test file). Replace with your preferred URL.
	default_mp3_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
	mp3_dest = os.path.join(snd_dir, "celebration.mp3")
	try:
		if not os.path.isfile(mp3_dest):
			download_mp3(default_mp3_url, mp3_dest)
		play_mp3(mp3_dest)
		return
	except Exception:
		# fall back to other methods
		pass
	if platform.system() == "Windows":
		try:
			import winsound
			# Prefer a cheerful system sound sometimes
			if random.random() < 0.4:
				winsound.MessageBeep(winsound.MB_OK)
				return
			# Otherwise play an ascending beep pattern
			for freq, dur in [(523, 100), (659, 100), (784, 120), (988, 160)]:
				winsound.Beep(freq, dur)
		except Exception:
			pass


def play_lose_sound():
	# Try WAV files first
	wavs = _wav_files_for("lose")
	if wavs:
		_play_wav(random.choice(wavs))
		return
	if platform.system() == "Windows":
		try:
			import winsound
			# Sometimes play a 'negative' system sound
			if random.random() < 0.4:
				winsound.MessageBeep(winsound.MB_ICONHAND)
				return
			# Descending beep/buzzer-like pattern
			for freq, dur in [(330, 150), (294, 150), (262, 220), (196, 260)]:
				winsound.Beep(freq, dur)
		except Exception:
			pass


def download_mp3(url: str, dest_path: str, show_progress: bool = False):
	"""Download an MP3 from `url` to `dest_path` using urllib. Overwrites if exists."""
	tmp = dest_path + ".part"
	with urllib.request.urlopen(url) as resp, open(tmp, "wb") as out:
		shutil.copyfileobj(resp, out)
	os.replace(tmp, dest_path)


def play_mp3(path: str):
	"""Play an mp3 using `playsound` if available, otherwise open with the OS default player."""
	# Prefer in-process playback using pygame (doesn't spawn external player)
	try:
		# initialize mixer if not already
		try:
			if not pygame.mixer.get_init():
				pygame.mixer.init()
		except Exception:
			# ignore init errors and continue
			pass
		# Try music playback (streaming)
		try:
			pygame.mixer.music.load(path)
			pygame.mixer.music.play()
			return True
		except Exception:
			# try Sound object as fallback
			try:
				snd = pygame.mixer.Sound(path)
				snd.play()
				return True
			except Exception:
				pass
	except Exception:
		pass

	# Secondary fallback: playsound (may be in-process depending on platform)
	try:
		from playsound import playsound
		try:
			playsound(path, block=False)
			return True
		except TypeError:
			playsound(path)
			return True
	except Exception:
		pass

	# If all methods fail, return False (do not open external players)
	return False


def generate_question(level: str):
	if level == "easy":
		a = random.randint(1, 9)
		b = random.randint(1, 9)
	elif level == "medium":
		# one single-digit and one double-digit
		if random.choice([True, False]):
			a = random.randint(1, 9)
			b = random.randint(10, 99)
		else:
			a = random.randint(10, 99)
			b = random.randint(1, 9)
	else:  # hard
		a = random.randint(10, 99)
		b = random.randint(10, 99)
	return a, b


def ask_questions(level: str, count: int, passing_pct: int = 70):
	correct = 0
	for i in range(1, count + 1):
		a, b = generate_question(level)
		ans = a * b
		while True:
			try:
				resp = input(f"Q{i}/{count}: {a} x {b} = ")
			except (EOFError, KeyboardInterrupt):
				print("\nExiting quiz.")
				return
			resp = resp.strip()
			if resp.lower() in ("q", "quit", "exit"):
				print("Quiz aborted.")
				return
			if resp == "":
				print("Please enter an answer (or 'q' to quit).")
				continue
			try:
				user = int(resp)
				break
			except ValueError:
				print("Invalid input — enter a number or 'q' to quit.")
		if user == ans:
			print("Correct!\n")
			correct += 1
		else:
			print(f"Wrong. Correct answer is {ans}\n")

	# result
	pct = int(correct * 100 / count) if count > 0 else 0
	print(f"Score: {correct}/{count} ({pct}%)")
	if pct >= passing_pct:
		print("You win! 🎉")
		play_win_sound()
	else:
		print("You lose. Try again! 😅")
		play_lose_sound()


def choose_level():
	print("Choose level:")
	print(" 1 - Easy (single-digit x single-digit)")
	print(" 2 - Medium (single-digit x double-digit)")
	print(" 3 - Hard (double-digit x double-digit)")
	while True:
		choice = input("Level (1/2/3) or q to quit: ").strip().lower()
		if choice in ("q", "quit", "exit"):
			return None
		if choice == "1":
			return "easy"
		if choice == "2":
			return "medium"
		if choice == "3":
			return "hard"
		print("Please choose 1, 2, or 3.")


def main():
	print("Multiply Game")
	print("Press Ctrl+C or enter 'q' any time to quit.")
	while True:
		level = choose_level()
		if level is None:
			print("Goodbye!")
			return
		try:
			cnt_raw = input("How many questions? (default 10): ").strip()
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye!")
			return
		if cnt_raw == "":
			count = 10
		else:
			try:
				count = int(cnt_raw)
				if count <= 0:
					print("Using default 10 questions.")
					count = 10
			except ValueError:
				print("Invalid number; using default 10.")
				count = 10

		ask_questions(level, count)
		again = input("Play again? (y/n): ").strip().lower()
		if again not in ("y", "yes"):
			print("Thanks for playing!")
			return


if __name__ == "__main__":
	main()
