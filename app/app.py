import Tkinter as tk

from prolog.search_engine_interface import SearchStub


class App(tk.Frame):
    """
    Simple gui for displaying questions and prolog predictions.
    """
    def __init__(self, master=tk.Tk(), search_engine=None):
        tk.Frame.__init__(self, master)

        self.question_text_var = tk.StringVar()
        self.question_text_var.set('Click "Start game" to begin.')
        self.question_label = tk.Label(self, textvariable=self.question_text_var)

        self.question_count_text_var = tk.StringVar()
        self.question_count_text_var.set('Questions asked: 0')
        self.question_count_label = tk.Label(self, textvariable=self.question_count_text_var)

        self.start_button = tk.Button(self, text='Start game', command=self.start_game)
        self.reset_button = tk.Button(self, text='Reset game', command=self.reset_game)

        self.yes_button = tk.Button(self, text='Yes', command=self.answer_yes)
        self.no_button = tk.Button(self, text='No', command=self.answer_no)

        self.question_count = 0
        self.search_engine = search_engine
        self.game_in_progress = False

        self.display_game_window()

    def start_game(self):
        question = self.search_engine.get_question()
        self.question_count = 0
        self.question_count_text_var.set('Questions asked: 0')

        self.game_in_progress = True
        self.question_text_var.set(question)

    def reset_game(self):
        pass

    def answer_yes(self):
        if self.game_in_progress:
            question, finished = self.search_engine.answer_yes()
            self.question_count += 1

            if finished:
                self.question_text_var.set('The person is: %s' % question)
                self.game_in_progress = False
            else:
                self.question_text_var.set(question)
                self.question_count_text_var.set('Questions asked: %d' % self.question_count)

    def answer_no(self):
        if self.game_in_progress:
            question = self.search_engine.answer_no()
            self.question_count += 1

            self.question_text_var.set(question)
            self.question_count_text_var.set('Questions asked: %d' % self.question_count)

    def display_game_window(self):
        self.grid(sticky=tk.N + tk.E + tk.W + tk.S)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.start_button.grid(row=0, column=0, sticky=tk.W)
        self.question_count_label.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.reset_button.grid(row=0, column=2, sticky=tk.E)

        self.question_label.grid(row=1, column=0, columnspan=3, rowspan=3, sticky=tk.W+tk.E)

        self.yes_button.grid(row=5, column=0, sticky=tk.W)
        self.no_button.grid(row=5, column=2, sticky=tk.E)


def main():
    prolog_engine = SearchStub()
    app = App(search_engine=prolog_engine)

    app.mainloop()


if __name__ == '__main__':
    main()
