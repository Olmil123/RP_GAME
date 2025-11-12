import os
import unittest

from game.models import Player, Enemy
from game.game import Game
from game.score import ScoreHandler, PlayerRecord
from game.settings import (
    PLAYER_LIVES,
    MODE_NORMAL,
    MODE_HARD,
    PAPER,
    STONE,
    SCISSORS,
    WIN,
    LOSE,
    DRAW,
    ATTACK_PAIRS_OUTCOME,
    SCORE_FILE,
)
from game.exceptions import GameOver, EnemyDown


class TestAttack(unittest.TestCase):
    def test_attack_basic(self):
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(PAPER, STONE)], WIN)
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(STONE, PAPER)], LOSE)
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(SCISSORS, PAPER)], WIN)
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(SCISSORS, STONE)], LOSE)
        self.assertEqual(ATTACK_PAIRS_OUTCOME[(STONE, STONE)], DRAW)


class TestModels(unittest.TestCase):
    def test_player_gameover(self):
        player = Player("Test")
        player.lives = 1
        with self.assertRaises(GameOver):
            player.decrease_lives()

    def test_enemydown(self):
        enemy = Enemy(level=1, mode=MODE_NORMAL)
        enemy.lives = 1
        with self.assertRaises(EnemyDown):
            enemy.decrease_lives()

    def test_enemymodes(self):
        enemy_normal = Enemy(level=2, mode=MODE_NORMAL)
        enemy_hard = Enemy(level=2, mode=MODE_HARD)
        self.assertGreater(enemy_hard.lives, enemy_normal.lives)


class TestGameLogic(unittest.TestCase):
    def test_game_fightwin(self):
        player = Player("Test")
        game = Game(player=player, mode=MODE_NORMAL)
        game.player.select_attack = lambda: PAPER
        game.enemy.select_attack = lambda: STONE
        result = game.fight()
        self.assertEqual(result, WIN)

    def test_game_fightloses(self):
        player = Player("Test")
        game = Game(player=player, mode=MODE_NORMAL)
        game.player.select_attack = lambda: STONE
        game.enemy.select_attack = lambda: PAPER
        result = game.fight()
        self.assertEqual(result, LOSE)

    def test_raises(self):
        player = Player("Test")
        game = Game(player=player, mode=MODE_NORMAL)
        game.enemy.lives = 1
        with self.assertRaises(EnemyDown):
            game.handle_fight_result(WIN)
        self.assertGreater(player.score, 0)

    def test_result_gameover(self):
        player = Player("Test")
        game = Game(player=player, mode=MODE_NORMAL)
        game.player.lives = 1
        with self.assertRaises(GameOver):
            game.handle_fight_result(LOSE)


class TestScoreSystem(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_scores.txt"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_score(self):
        handler = ScoreHandler(self.test_file)

        r1 = PlayerRecord("Sasha", MODE_NORMAL, 10)
        r2 = PlayerRecord("Sasha", MODE_HARD, 20)
        r3 = PlayerRecord("Olena", MODE_NORMAL, 15)

        handler.game_record.add_record(r1)
        handler.game_record.add_record(r2)
        handler.game_record.add_record(r3)
        handler.save()
        handler2 = ScoreHandler(self.test_file)
        records = handler2.game_record.records

        self.assertEqual(len(records), 3)
        found = any(
            rec.name == "Sasha" and rec.mode == MODE_NORMAL and rec.score == 10
            for rec in records
        )
        self.assertTrue(found)

    def test_update_record(self):
        handler = ScoreHandler(self.test_file)
        r1 = PlayerRecord("Sasha", MODE_NORMAL, 10)
        r2 = PlayerRecord("Sasha", MODE_NORMAL, 30)
        handler.game_record.add_record(r1)
        handler.game_record.add_record(r2)
        handler.save()
        handler2 = ScoreHandler(self.test_file)
        records = handler2.game_record.records
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].score, 30)


if __name__ == "__main__":
    unittest.main()
