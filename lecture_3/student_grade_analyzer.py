def texter(text: str) -> str:
    """
    Функция очищает вводимый и возвращает уже форматированный текст

    :param text: текстовая строка пользователя
    :return: очищенный и отформатированный текст
    """
    return ' '.join(text.strip().split()).title()


def new_student(name: str, students: list) -> None:
    """
    Добавление нового студента

    :param name: имя студента
    :param students: список словарей вида {'имя': [оценки]}
    :return: добавление словаря в list
    """
    if any(name in x for x in students):
        print('Student with this name already exists')
        return None
    else:
        students.append({name: list()})
        return None


def who_is_student(name: str, students: list) -> int:
    """
    Поиск индекса элемента в списке с данными определенного студента

    :param name: имя студента
    :param students: список словарей
    :return: индекс для поиска в словаре
    """
    for i, d in enumerate(students):
        if name in d:
            return i
        else:
            return -1


def add_grades(name: str, students: list) -> None:
    """
    Добавление оценок существующему студенту

    :param name: имя студента
    :param students: список словарей
    :return: None, добавление в список оценок студентов или вывод сообщения об ошибке
    """
    if any(name in x for x in students):
        while True:
            tmp_grades = input('Enter a grade (or \'done\' to finish): ').lower().strip()
            if tmp_grades == 'done':
                break
            elif tmp_grades.isdigit() and 0 < int(tmp_grades) <= 100:
                students[who_is_student(name, students)][name].append(int(tmp_grades))
            else:
                print('Invalid input. Please enter a correct number.')
        return None
    else:
        print('Student with this name doesn\'t existing')
        return None


def avg_students(students: list[dict[str, list[int]]], i):
    """
    Получение данных о показателях студентов, сравнение показателей.
    Учитывает случай, при котором несколько студентов имеют одинаковые средние значения

    :param students: список словарей, в каждом словаре по ключу доступен список оценок
    :param i: 1 - max avg, 2 - min avg, 3 - over avg
    :return:
        i == 1: кортеж (строка с именем/именами, максимальное среднее значение)
        i == 2: кортеж (строка с именем/именами, минимальное среднее значение)
        i == 3: общее среднее значение (float)
    иначе: None
    """

    averages = []
    for student_dict in students:
        for name, grades in student_dict.items():
            if not grades: # если нет оценок
                continue
            avg = round(sum(grades) / len(grades), 1)
            averages.append((name, avg))
    if not averages: # если нет ни одного студента с оценками
        return None
    if i == 1: # максимум
        max_value = max(avg for _, avg in averages)
        top_names = [name for name, avg in averages if avg == max_value]
        names_str = ", ".join(top_names)
        return names_str, max_value
    elif i == 2: # минимум
        return min(averages, key=lambda x: x[1])
    elif i == 3: # общее среднее
        return round(sum(avg for _, avg in averages) / len(averages), 1)
    else:
        return None


menu_txt = """
--- Student Grade Analyzer ---
1. Add a new student
2. Add a grades for a student
3. Show report (all students)
4. Find top performed
5. Exit"""
students = []

while True:
    print(menu_txt)
    command = input('Enter your choice: ')
    if command == '1':
        new_student(texter(input('Enter student name: ')), students)
    elif command == '2':
        add_grades(texter(input('Enter student name: ')), students)
    elif command == '3':
        try:
            print('''
            --- Student Report ---''')
            for i in students:
                for key, value in i.items():
                    if len(value) == 0:
                        print(f"{key}'s average grade is N/A.")
                    else:
                        print(f"{key}'s average grade is {round(sum(value) / len(value))}")
            print('--------------------------\n'
                  f'Max Average: {avg_students(students, 1)[1]}\n'
                  f'Min Average: {avg_students(students, 2)[1]}\n'
                  f'Overall Average: {avg_students(students, 3)}')
        except TypeError:
            print('No student data available or no grades available..')
    elif command == '4':
        try:
            print(f'The student with the highest average is {avg_students(students, 1)[0]} with a grade of {avg_students(students, 1)[1]}')
        except TypeError:
            print('No student data available or no grades available')
    elif command == '5':
        print('Exiting program')
        break
    else:
        print('Please enter a valid choice')
