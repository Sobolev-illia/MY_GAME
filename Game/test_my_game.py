import unittest
from my_game import Ball
from my_game import Platform
from my_game import Block

class TestBallMotion(unittest.TestCase):
    def setUp(self):
        self.ball = Ball()
        self.platform = Platform()
        self.block1 = Block(1303, 275)
        self.block2 = Block(445, 275)

    def test_collision_with_platform_top(self):
        # Шарик летит влево вниз и сталкивается с верхней частью платформы
        self.assertEqual(self.ball.detect_collision(-1, 1, self.platform), (-1, -1))

    def test_collision_with_platform_bottom(self):
        # Шарик летит вправо вниз и сталкивается с верхней частью платформы
        self.assertEqual(self.ball.detect_collision(1, 1, self.platform), (1, -1))

    def test_collision_with_block_top(self):
        # Шарик летит влево вверх и сталкивается с нижней частью блока
        self.assertEqual(self.ball.detect_collision(-1, -1, self.block1), (-1, 1))

    def test_collision_with_block_bottom(self):
        # Шарик летит вправо вверх и сталкивается с нижней частью блока
        self.assertEqual(self.ball.detect_collision(1, -1, self.block2), (1, 1))

if __name__ == '__main__':
    unittest.main()
