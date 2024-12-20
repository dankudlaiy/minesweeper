import random
from sentence import Sentence


class MinesweeperAI:
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.moves_made = set()

        self.mines = set()
        self.safes = set()

        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # removing empty sentences
        for sent in self.knowledge:
            if len(sent.cells) == 0:
                self.knowledge.remove(sent)

        # removing safes and mines from knowledge
        for sent in self.knowledge:
            for safe in self.safes:
                if safe in sent.cells.copy():
                    print(f'removing new safe {safe} from {sent.cells} = {sent.count}\n')
                    sent.cells.difference_update({safe})
            for mine in self.mines:
                if mine in sent.cells.copy():
                    print(f'removing new mine {mine} from {sent.cells} = {sent.count}\n')
                    sent.cells.difference_update({mine})
                    sent.count -= 1

        # add a new sentence to the knowledge
        neighbors = []
        if cell[0] == 0:
            if cell[1] == 0:  # (0,0) corner
                for n1 in range(0, 2):
                    for n2 in range(0, 2):
                        neighbors.append((cell[0] + n1, cell[1] + n2))
            elif cell[1] == self.width - 1:  # (0,7) corner
                for n1 in range(0, 2):
                    for n2 in range(-1, 1):
                        neighbors.append((cell[0] + n1, cell[1] + n2))
            else:  # (0,j) row
                for n1 in range(0, 2):
                    for n2 in range(-1, 2):
                        neighbors.append((cell[0] + n1, cell[1] + n2))
        elif cell[0] == self.height - 1:
            if cell[1] == 0:  # (7,0) corner
                for n1 in range(-1, 1):
                    for n2 in range(0, 2):
                        neighbors.append((cell[0] + n1, cell[1] + n2))
            elif cell[1] == self.width - 1:  # (7,7) corner
                for n1 in range(-1, 1):
                    for n2 in range(-1, 1):
                        neighbors.append((cell[0] + n1, cell[1] + n2))
            else:  # (7,j) row
                for n1 in range(-1, 1):
                    for n2 in range(-1, 2):
                        neighbors.append((cell[0] + n1, cell[1] + n2))
        elif (cell[1] == 0) and (cell[0] > 0) and (cell[0] < self.width - 1):  # (i,0) column
            for n1 in range(-1, 2):
                for n2 in range(0, 2):
                    neighbors.append((cell[0] + n1, cell[1] + n2))
        elif (cell[1] == self.height - 1) and (cell[0] > 0) and (cell[0] < self.width - 1):  # (i,7) column
            for n1 in range(-1, 2):
                for n2 in range(-1, 1):
                    neighbors.append((cell[0] + n1, cell[1] + n2))
        else:
            for n1 in range(-1, 2):
                for n2 in range(-1, 2):
                    neighbors.append((cell[0] + n1, cell[1] + n2))

        for neigh in neighbors:
            if neigh in self.safes:
                neighbors.remove(neigh)
            elif neigh in self.mines:
                if count > 0:
                    count -= 1
                    neighbors.remove(neigh)
        self.knowledge.append(Sentence(neighbors, count))
        print(f'adding knowledge: {self.knowledge[-1].cells}={self.knowledge[-1].count}')

        for sent in self.knowledge:
            aux = []

            if sent.count == 0:
                for newsafe in sent.cells.copy():
                    self.mark_safe(newsafe)
                    aux.append(newsafe)
                self.knowledge.remove(sent)

            elif sent.count == len(sent.cells):
                aux = []
                for newmine in sent.cells.copy():
                    self.mark_mine(newmine)
                    aux.append(newmine)
                self.knowledge.remove(sent)

        for sent in self.knowledge:
            if len(sent.cells) == 0:
                self.knowledge.remove(sent)

        # add any new sentences from inference to the knowledge base
        # {A,B,C,D,E} = 3 and {A,B,C} = 1 => {D,E} = 2
        for sent0 in self.knowledge:
            for sent1 in self.knowledge:
                if sent0.cells < sent1.cells:
                    print(f'getting infered knowledge from {sent0.cells} = {sent0.count} and {sent1.cells} = {sent1.count}\n')
                    self.knowledge.append(Sentence(sent1.cells.difference(sent0.cells), sent1.count - sent0.count))
                    self.knowledge.remove(sent1)
                    print(f'infered knowledge added:{self.knowledge[-1].cells} = {self.knowledge[-1].count}. Removing {sent1.cells} = {sent1.count}')

    def make_safe_move(self):
        if len(self.safes) - len(self.moves_made) > 0:
            return self.safes.difference(self.moves_made).pop()

    def make_random_move(self):
        if len(self.safes) - len(self.moves_made) < 1:
            auxcell = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            while (auxcell not in self.moves_made.union(self.mines)) and (
                    len(self.safes) + len(self.mines) < (self.height - 1) * (self.width - 1)):
                return auxcell
