import sys
import time

class Roll():
    cnt = 0
    rolls = ["-", "\\", "|", "/"]

    def get_roll(self):
        res = self.rolls[self.cnt]
        self.increment_cnt()
        return res

    def increment_cnt(self):
        self.cnt += 1
        if self.cnt == 4:
            self.cnt = 0


roll = Roll();


def progress_bar(progress):
    bar_length = 20
    filled_length = int(progress * bar_length)
    bar = '#' * (filled_length - 1) + roll.get_roll() + '-' * (bar_length - filled_length)
    percent = int(progress * 100)
    sys.stdout.write('\r')
    sys.stdout.write(f"[{bar}] {percent}%")
    sys.stdout.flush()


# Example usage:
for i in range(101):
    progress_bar(i / 100)
    time.sleep(0.1)
