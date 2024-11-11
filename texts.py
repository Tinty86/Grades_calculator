
class LinkedList:
    head = None
    class Node:
        grade = None
        weight = None
        next_node = None
        def __init__(self, grade:int, weight:float, next_node=None):
            self.grade = grade
            self.weight = weight
            self.next_node = next_node 
    def append(self, grade, weight):
        if not self.head:
            self.head = self.Node(grade, weight)
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        node.next_node = self.Node(grade, weight)
    def delete(self):
        if not self.head:
            print("Нет данных для удаления")
            return
        node = self.head
        while node.next_node:
            prev_node = node
            node = node.next_node
        prev_node.next_node = None 
    def return_head(self):
        return self.head

grades_path = "C:\\Users\\User\\.grades"
start_message = "Напишите оценку и вес через точку с запятой (чтобы закончить напиши стоп) ->: "
final_grade = "Напишите оценку, с помощью которой вы хотите узнать итоговую оценку, и её вес через точку с запятой (если вы хотите остановить ввод напишите \"стоп\") ->: "
not_found_file = "Файл не найден, проверьте название файла, либо правильность написания предмета -"
wish_of_saving = "Хотите ли вы сохранить оценки в файле? ->: "