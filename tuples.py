class Tuples:
    stop_words = ("stop","save","end", "enough", "s", "закончить","остановить","конец","стоп", "достаточно", "с", "n")
    agreement_words = ("ok","yes","yeah","yea","yeap","yep","sure", "of course","y", "lf", "да", "ага", "давай", "ок", "окей", "конечно")
    del_words = ("delete last", "delete the last one", "delete last one", "delete", "del", "d", "удалить", "удалить прошлое", "удалить предыдущее", "удал", "уд")

    def all_lists(self) -> tuple:
        return self.stop_words, self.agreement_words, self.del_words

    def return_stop_words(self):
        return self.stop_words

    def return_agreement_words(self):
        return self.agreement_words

    def return_del_words(self):
        return self.del_words

def return_list(which_list: str) -> tuple:
    lists = Tuples()
    if which_list == "all":
        return lists.all_lists()
    elif which_list == "stop_words":
        return lists.return_stop_words()
    elif which_list == "agreement_words":
        return lists.return_agreement_words()
    elif which_list == "del_words":
        return lists.return_del_words()
    else:
        raise ValueError("Unknown list type")