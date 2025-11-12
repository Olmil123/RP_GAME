from game.models import Player, Enemy
from game.exceptions import GameOver, EnemyDown
from game.score import ScoreHandler, PlayerRecord
from game.settings import (
    ATTACK_PAIRS_OUTCOME,
    WIN,
    DRAW,
    LOSE,
    POINTS_FOR_FIGHT,
    POINTS_FOR_KILLING,
    SCORE_FILE,
    MODE_HARD,
    HARD_MODE_MULTIPLIER,
)


class Game:
    def __init__(self, player: Player, mode: str):
        self.player = player
        self.mode = mode
        self.enemy = Enemy(level=1, mode=mode)
        print(f"Game started! Mode: {self.mode}. Enemy level: {self.enemy.level}")

    def create_enemy(self):
        new_level = self.enemy.level + 1
        self.enemy = Enemy(level=new_level, mode=self.mode)
        print(f"New enemy appeared!! Level: {self.enemy.level}")

    def fight(self) -> int:
        player_attack = self.player.select_attack()
        enemy_attack = self.enemy.select_attack()
        print(f"You chose: {player_attack}")
        print(f"Enemy chose: {enemy_attack}")
        result = ATTACK_PAIRS_OUTCOME[(player_attack, enemy_attack)]

        if result == WIN:
            print("YUUPIIII!!! You win this round!")
        elif result == LOSE:
            print("You lost this round! 0_0 ")
        else:
            print("It's a draw!")
        return result

    def handle_fight_result(self, result: int):
        if result == WIN:
            self.player.add_score(self._calculate_points(POINTS_FOR_FIGHT))
            self.enemy.decrease_lives()
        elif result == LOSE:
            self.player.decrease_lives()
        elif result == DRAW:
            print("Try again!")

    def play(self):
        while True:
            try:
                result = self.fight()
                self.handle_fight_result(result)

            except EnemyDown:
                print("Enemy is defeated! You get extra points for killing!!")
                self.player.add_score(self._calculate_points(POINTS_FOR_KILLING))
                self.create_enemy()

            except GameOver:
                print("GAME OVER!!")
                print(f"Your final score: {self.player.score}")
                self.save_score()
                break

    def save_score(self):
        handler = ScoreHandler(SCORE_FILE)
        record = PlayerRecord(self.player.name, self.mode, self.player.score)
        handler.game_record.add_record(record)
        handler.save()
        handler.display()

    def _calculate_points(self, base_points: int) -> int:
        if self.mode == MODE_HARD:
            return base_points * HARD_MODE_MULTIPLIER
        return base_points
