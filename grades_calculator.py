# Now on Git
import os
from os import mkdir 
from art import tprint
from tuples import return_list
import texts

LinkedList = texts.LinkedList

def real_grades(stop_words: tuple, del_words: tuple):
    # Реальные оценки и веса
    inp = ""
    linked_list_with_all = LinkedList()
    while inp.lower() not in stop_words:
        inp = input(texts.start_message)
        if inp.lower() in del_words:
            linked_list_with_all.delete()
            print("Предыдущая оценка удалена")
            continue
        if inp.lower() not in stop_words:
            grade = inp.split(";")[0]
            weight = inp.split(";")[1]
            linked_list_with_all.append(grade, weight)
            
    head = linked_list_with_all.return_head()
    return head

def saving_data(head_of_linked_list:texts.LinkedList, path:str):
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
    if len(files) > 0:
        for i in files:
            if object_name[:2] == i[:2]: 
                if input(f"Может вы имели ввиду \"{i}\"? ->: ") in agreement_words:
                    return f"{texts.grades_path}\\{i}"
    return ""

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

# Проверочная оценка

def view_in_future(numerator:float, denominator:float, unreal_grade:str):
    grade = float(unreal_grade.split(";")[0])
    weight = float(unreal_grade.split(";")[1])

    denominator = denominator + weight
    numerator = numerator + grade * weight

    hypothetical_res_grade = numerator / denominator

    return hypothetical_res_grade

# Подсчет по формуле

def calculating(head: texts.LinkedList):
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

# main

def main(stop_words: tuple, agreement_words: tuple, path:str, object_name: str, del_words: tuple):

    if input("Есть ли новые оценки? ->: ").lower() in agreement_words: 
        head_of_linked_list = real_grades(stop_words, del_words)
        if input(texts.wish_of_saving).lower() in agreement_words: saving_data(head_of_linked_list, path)

    else: 
        if os.path.exists(path): head_of_linked_list = collecting_data(path)
        else: 
            path = maybe_another_file_name(object_name, agreement_words)
            if path == "":
                print(f"{texts.not_found_file} \"{object_name}\"") 
                exit()
            head_of_linked_list = collecting_data(path)

    numerator, denominator = calculating(head_of_linked_list)

    res_grade = round(numerator / denominator, 2)
    print(f"Ваша нынешняя оценка - {res_grade}")

    unreal_grade = ""
    while unreal_grade not in stop_words:
        unreal_grade = input(texts.final_grade)
        if unreal_grade in stop_words: exit()
        hypothetical_res_grade = view_in_future(numerator, denominator, unreal_grade)
        print(f"Гипотетическая итоговая оценка - {hypothetical_res_grade}")

if __name__ == "__main__":
    # art
    tprint("Welcome to grades calculator!")
    # Переменные
    object_name = input("Укажите название предмета ->: ")
    path = f"{texts.grades_path}\\{object_name}.txt"

    stop_words, agreement_words, del_words = return_list(which_list="all")

    main(stop_words,agreement_words, path, object_name, del_words)