from abc import ABCMeta, abstractmethod
from random import randint


class SearchInterface(object):
    @abstractmethod
    def get_question(self):
        pass

    @abstractmethod
    def answer_yes(self):
        pass

    @abstractmethod
    def answer_no(self):
        pass


class SearchStub(SearchInterface):
    def answer_no(self):
        num = randint(0, 2)
        if num == 0:
            return "Does this person have moustache?", False
        elif num == 1:
            return "Does this person play piano?", False
        else:
            return "Does this person dance?", False

    def answer_yes(self):
        num = randint(0, 2)
        if num == 0:
            return "Does this person won oscar?", False
        elif num == 1:
            return "Does this person play football?", False
        else:
            return "Warhol", True

    def get_question(self):
        return "Is this person a male?"
