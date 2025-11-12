from game.settings import PLAYER_LIVES, ALLOWED_ATTACKS, HARD_MODE_MULTIPLIER, MODE_HARD
from game.exceptions import GameOver, EnemyDown
from random import choice


class Player:
    def __init__(self, name: str):
        self.name = name
        self.lives = PLAYER_LIVES
        self.score = 0

    def select_attack(self) -> str:
        while True:
            print("Choose in attack:")
            for key, value in ALLOWED_ATTACKS.items():
                print(f"{key} - {value}")
            choice = input("Your choice: ")
            if choice in ALLOWED_ATTACKS:
                return ALLOWED_ATTACKS[choice]
            else:
                print("Incorrect input, please try again!!")

    def decrease_lives(self):
        self.lives -= 1
        print(f"You have lives remaining: {self.lives}")
        if self.lives <= 0:
            raise GameOver("The player has run out of lives:(")

    def add_score(self, points: int):
        self.score += points
        print(f"Your score: {self.score}")


class Enemy:
    def __init__(self, level: int, mode: str):
        self.level = level
        self.mode = mode

        lives = level
        if mode == MODE_HARD:
            lives *= HARD_MODE_MULTIPLIER
        self.lives = lives

    def select_attack(self) -> str:
        return choice(list(ALLOWED_ATTACKS.values()))

    def decrease_lives(self):
        self.lives -= 1
        print(f"The enemy has lives left: {self.lives}")

        if self.lives <= 0:
            raise EnemyDown("The enemy is defeated WIN!")
