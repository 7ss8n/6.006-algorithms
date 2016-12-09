import unittest
import random
import time
from doodle import double_kill, triple_kill

####################################################################################################
################################      PLEASE DO NOT MODIFY        ##################################
####################################################################################################
class Ghost:
    def __init__(self, moves):
        self.moves = moves
        self.lives_lost = 0

    def __repr__(self):
        if self.alive():
            return ''.join(self.moves[:self.lives_lost]) + ' -> ' + ''.join(self.moves[self.lives_lost:])
        else:
            return 'DEAD'

    def alive(self):
        return self.lives_lost < len(self.moves)

def play(ghosts, moves, vis):
    if vis:
        for i, g in enumerate(ghosts):
            print('ghost '+str(i) + ': ' + str(g))

    for move in moves:
        if vis:
            print('----- '+move+' -----')
        for i, g in enumerate(ghosts):
            if g.lives_lost < len(g.moves) and g.moves[g.lives_lost] == move:
                g.lives_lost += 1
            if vis:
                print('ghost '+str(i) + ': ' + str(g))

def generate(N, alphabet):
    return [random.choice(alphabet) for x in range(N)]

##########################################################################################
################################      TEST CASES        ##################################
##########################################################################################
'''
    You may set the third argument of play() to True in each of these tests to see a very crude simulation of the game.
'''

class TestDouble(unittest.TestCase):
    def test_double_basic(self):
        moves1 = ['A', 'B', 'B', 'B']
        moves2 = ['C', 'B', 'B', 'B', 'B']
        student_res = double_kill(moves1, moves2)
        expect_len = 6
        ghost1 = Ghost(moves1)
        ghost2 = Ghost(moves2)
        play([ghost1, ghost2], student_res, False)
        self.assertFalse(ghost1.alive(), "sequence did not kill ghost 1")
        self.assertFalse(ghost2.alive(), "sequence did not kill ghost 2")
        self.assertEqual(len(student_res), expect_len, "not the optimal sequence")

    def test_double_long(self):
        moves1 = ['A', 'B', 'B', 'B', 'D', 'A', 'D', 'C', 'A', 'B', 'C', 'A', 'D', 'B', 'A', 'A', 'A', 'B']
        moves2 = ['C', 'B', 'B', 'B', 'B', 'C', 'B', 'B', 'B', 'B', 'C', 'B', 'B', 'B', 'B', 'A', 'A']
        student_res = double_kill(moves1, moves2)
        expect_len = 26
        ghost1 = Ghost(moves1)
        ghost2 = Ghost(moves2)
        play([ghost1, ghost2], student_res, False)
        self.assertFalse(ghost1.alive(), "sequence did not kill ghost 1")
        self.assertFalse(ghost2.alive(), "sequence did not kill ghost 2")
        self.assertEqual(len(student_res), expect_len, "not the optimal sequence")

    def test_double_timing(self):
        alphabet = ['A', 'B', 'C', 'D']
        N = 1000
        for i in range(3):
            moves1 = generate(N, alphabet)
            moves2 = generate(N, alphabet)
            start_time = time.time()
            student_res = double_kill(moves1, moves2)
            end_time = time.time()
            ghost1 = Ghost(moves1)
            ghost2 = Ghost(moves2)
            play([ghost1, ghost2], student_res, False)
            self.assertFalse(ghost1.alive(), "sequence did not kill ghost 1")
            self.assertFalse(ghost2.alive(), "sequence did not kill ghost 2")
            print("double_kill test took", end_time - start_time, "seconds")
            self.assertTrue(end_time - start_time < 3.0, "double_kill takes too long!")

class TestTriple(unittest.TestCase):
    def test_triple_basic(self):
        moves1 = ['C', 'B', 'A', 'B', 'A', 'D']
        moves2 = ['B', 'A', 'B', 'A', 'D', 'C', 'D']
        moves3 = ['D', 'C', 'D', 'A', 'A']
        student_res = triple_kill(moves1, moves2, moves3)
        ghost1 = Ghost(moves1)
        ghost2 = Ghost(moves2)
        ghost3 = Ghost(moves3)
        play([ghost1, ghost2, ghost3], student_res, False)
        expect_len = 10
        self.assertFalse(ghost1.alive(), "sequence did not kill ghost 1")
        self.assertFalse(ghost2.alive(), "sequence did not kill ghost 2")
        self.assertFalse(ghost3.alive(), "sequence did not kill ghost 3")
        self.assertEqual(len(student_res), expect_len, "not the optimal sequence")


    def test_triple_long(self):
        moves1 = ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'D', 'C']
        moves2 = ['B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'D', 'D']
        moves3 = ['D', 'C', 'D', 'A', 'B', 'A', 'B', 'A', 'B', 'C', 'D', 'C', 'D', 'A', 'D', 'C', 'C']
        student_res = triple_kill(moves1, moves2, moves3)
        ghost1 = Ghost(moves1)
        ghost2 = Ghost(moves2)
        ghost3 = Ghost(moves3)
        play([ghost1, ghost2, ghost3], student_res, False)
        expect_len = 27
        self.assertFalse(ghost1.alive(), "sequence did not kill ghost 1")
        self.assertFalse(ghost2.alive(), "sequence did not kill ghost 2")
        self.assertFalse(ghost3.alive(), "sequence did not kill ghost 3")
        self.assertEqual(len(student_res), expect_len, "not the optimal sequence")

    def test_triple_timing(self):
        alphabet = ['A', 'B', 'C', 'D']
        N = 100
        for i in range(3):
            moves1 = generate(N, alphabet)
            moves2 = generate(N, alphabet)
            moves3 = generate(N, alphabet)
            start_time = time.time()
            student_res = triple_kill(moves1, moves2, moves3)
            end_time = time.time()
            ghost1 = Ghost(moves1)
            ghost2 = Ghost(moves2)
            ghost3 = Ghost(moves3)
            play([ghost1, ghost2, ghost3], student_res, False)
            self.assertFalse(ghost1.alive(), "sequence did not kill ghost 1")
            self.assertFalse(ghost2.alive(), "sequence did not kill ghost 2")
            self.assertFalse(ghost3.alive(), "sequence did not kill ghost 3")
            print("triple_kill test took", end_time - start_time, "seconds")
            self.assertTrue(end_time - start_time < 10.0, "triple_kill takes too long!")


if __name__ == '__main__':
    unittest.main()
