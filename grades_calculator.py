
import os
from os import mkdir 
from tuples import return_list
import texts
import classes
from single_functions import *

LinkedList = classes.LinkedList

def collecting_grades(stop_words: tuple, del_words: tuple, numerator: float = 0, denominator: float = 0, linked_list_with_all: LinkedList = None, first_call = True):
    inp = ""
    if first_call:
        linked_list_with_all = LinkedList()
        print("Для того чтобы удалить оценку напишите \"удалить\"")
    while inp.lower() not in stop_words:
        inp = input(texts.grade_message)
        if inp.lower() in del_words:
            linked_list_with_all.delete()
            os.system("")
            print("Предыдущая оценка удалена")
            continue
        if inp.lower() not in stop_words:
            grade = inp.split(";")[0]
            weight = inp.split(";")[1]
            if not can_var_be_float(grade) or not can_var_be_float(weight): 
                write_it_in_red("Значения должны быть числами!!!")
                return collecting_grades(stop_words, del_words, numerator, denominator, linked_list_with_all, first_call = False)
            linked_list_with_all.append(grade, weight)
            if denominator > 0:
                hypothetical_res_grade = view_in_future(stop_words, del_words, numerator, denominator, f"{grade};{weight}")
                print(f"{texts.hypothetical_grade} {hypothetical_res_grade}")
    head = linked_list_with_all.return_head()
    if not head: 
        write_it_in_red(texts.must_init)
        collecting_grades(stop_words, del_words, numerator, denominator)

    return head

def saving_data(head_of_linked_list:classes.LinkedList, path:str):
    node = head_of_linked_list
    if not os.path.exists(texts.grades_path): mkdir(texts.grades_path)
    if not os.path.exists(path): format = "w" 
    else: format = "a"
    
    with open(path, format) as output_file:
        while node.next_node:
            output_file.write(f"{node.grade};{node.weight}\n")
            node = node.next_node
        output_file.write(f"{node.grade};{node.weight}\n")

# Может вы имели ввиду другое имя файла?

def maybe_another_file_name(object_name:str, agreement_words:tuple):
    files = tuple(os.listdir(texts.grades_path))
    for i in files:
        if object_name[:2] == i[:2].lower(): 
            if input(f"Может вы имели ввиду \"{i}\"? ->: ") in agreement_words:
                return f"{texts.grades_path}\\{i}"
    return f"{texts.grades_path}\\{object_name}.txt"

# Получение данных из файла

def collecting_data(path:str):
    linked_list_with_all = LinkedList()
    with open(path) as input_file:
        for i in input_file.readlines():
            i = i.splitlines()[0]
            grade = i.split(";")[0]
            weight = i.split(";")[1]
            linked_list_with_all.append(grade, weight)

    head = linked_list_with_all.return_head()
    return head

def view_in_future(stop_words: tuple, del_words: tuple, numerator:float, denominator:float, unreal_grade:str):
    grade = unreal_grade.split(";")[0]
    weight = unreal_grade.split(";")[1]

    if not can_var_be_float(grade) or not can_var_be_float(weight):
        write_it_in_red("Значения должны быть числами!!!")
        work_with_fiction(stop_words, del_words, numerator, denominator, first_call=False)

    grade = float(grade)
    weight = float(weight)

    denominator = denominator + weight
    numerator = numerator + grade * weight

    hypothetical_res_grade = numerator / denominator

    return hypothetical_res_grade

def calculating(head: classes.LinkedList):
    node = head
    weights_list = [] 
    numerator = 0
    while node.next_node:
        grade = node.grade
        weight = node.weight
        numerator += int(grade) * float(weight)
        weights_list.append(float(weight))
        node = node.next_node

    grade = node.grade
    weight = node.weight
    numerator += int(grade) * float(weight)
    weights_list.append(float(weight))

    denominator = float(sum(weights_list))

    return numerator, denominator

def copy_file(path:str):
    with open(path) as input_file:
        input_text = input_file.read()
    with open(f"{texts.grades_path}//temp.txt", "a+") as output_file:
        output_file.write(input_text)

def work_with_fiction(stop_words: tuple, del_words: tuple, numerator: float, denominator: float, user_choice = 1, first_call = True):
    if first_call:
        user_choice = int(input(texts.check_choice))
        if user_choice not in (1,2):
            write_it_in_red("Недопустимый ответ. Напишите вариант ответа 1 или 2")
            while True:
                user_choice = int(input(texts.check_choice))
                if user_choice in (1,2): break
    if user_choice == 1:
        unreal_grade = ""
        while unreal_grade not in stop_words:
            unreal_grade = input(texts.final_grade)
            if unreal_grade not in stop_words:
                hypothetical_res_grade = view_in_future(stop_words, del_words, numerator, denominator, unreal_grade)
                print(f"{texts.hypothetical_grade} {hypothetical_res_grade}")
    else:
        collecting_grades(stop_words, del_words, numerator, denominator)

def main(first_call: bool = True, object_name = ""):

    if first_call:
        object_name = input("Укажите название предмета ->: ").lower()
    
    path = f"{texts.grades_path}\\{object_name}.txt"

    stop_words, agreement_words, del_words = return_list(which_list="all")

    if not os.path.exists(path): path = maybe_another_file_name(object_name, agreement_words)

    isTemp = False

    if input("Есть ли новые оценки? ->: ").lower() in agreement_words: 
        head_of_linked_list = collecting_grades(stop_words, del_words)
        if input(texts.wish_of_saving).lower() in agreement_words: saving_data(head_of_linked_list, path)
        else: 
            isTemp = True
            if os.path.exists(path): copy_file(path)
            path = f"{texts.grades_path}\\temp.txt"
            saving_data(head_of_linked_list, path)

    if not os.path.exists(path): 
        write_it_in_red(texts.must_init)
        main(first_call = False, object_name = object_name)

    head_of_linked_list = collecting_data(path)

    if isTemp:
        os.remove(path)

    numerator, denominator = calculating(head_of_linked_list)

    res_grade = round(numerator / denominator, 2)
    print(f"Ваша нынешняя оценка - {res_grade}")

    work_with_fiction(stop_words, del_words, numerator, denominator)

if __name__ == "__main__":
    write_it_in_red(texts.start_message)
    main(first_call=True)
