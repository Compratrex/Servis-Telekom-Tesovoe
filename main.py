import datetime
from Employee import Employee, EmployeeTaskSystem

# Опрееляем всех по задаче:
ivanov = Employee(1, "Иванов", ['SDH', 'PDH', 'WDM'], 3, datetime.date(2024, 2, 2),
                  [datetime.date(2024, 2, 5), datetime.date(2024, 2, 15)])

petrov = Employee(2, "Петров", ["СПД", "Сервера"], 6, datetime.date(2024, 1, 30),
                  [datetime.date(2024, 2, 7), datetime.date(2024, 2, 9)])

sidorov = Employee(3, "Сидоров", ["ОбТС", "PDH"], 3, datetime.date(2024, 2, 2))

rabinovich = Employee(4, "Рабинович", ["Сервера", "WDM"], 5, datetime.date(2024, 1, 30),
                      [datetime.date(2024, 2, 12), datetime.date(2024, 2, 15)])

zozo = Employee(5, "Зозо", ["ОбТС", "СПД"], 3, datetime.date(2024, 1, 31),
                [datetime.date(2024, 2, 7), datetime.date(2024, 2, 9)])

# Добавляем для тестирования еще тестовых сотрудников
test_object_1 = Employee(6, "test_1", ["PhpAdmin", "Nginx"], 3, datetime.date(2024, 1, 31),
                         [datetime.date(2024, 2, 7), datetime.date(2024, 2, 9)])

test_object_2 = Employee(7, "test_2", ["PhpAdmin", "Nginx"], 3, datetime.date(2024, 1, 31),
                         [datetime.date(2024, 2, 7), datetime.date(2024, 2, 9)])

petrov_2 = Employee(8, "Петров 2", ["СПД", "Сервера"], 6, datetime.date(2024, 1, 30),
                  [datetime.date(2024, 2, 8), datetime.date(2024, 2, 9)])

# Определяем нашу систему
system = EmployeeTaskSystem()
# Добавляем всех в нашу систему
system.add_employee(ivanov)
system.add_employee(petrov)
system.add_employee(sidorov)
system.add_employee(rabinovich)
system.add_employee(zozo)
system.add_employee(test_object_1)
system.add_employee(test_object_2)
system.add_employee(petrov_2)


# проводим тесты.
def tech_tests():
    # Пробуем с PDH и датой обращения 03.02.24. Тут подходят два сотрудника: Сидоров и Иванов. Дата обращения последняя
    # одинаковая, но так как Иванов 1 в спсике, то задача должна быть определенна ему
    assert "Иванов" == system.get_employee_who_do_task(datetime.date(2024, 2, 3), "PDH")
    # Пробуем с ОбТС и датой обращения 09.02.24. Тут подходят два сотрудника: Зозо и Сидоров. Дата обращения последняя
    # разная, но Зозо в отпуске, поэтому передаем Сидорову, который работает 24/7 без отпусков.
    assert "Сидоров" == system.get_employee_who_do_task(datetime.date(2024, 2, 9), "ОбТС")
    # А что если дату поставим 03.02.24? Тогда будет Зозо, потому что у него самая давняя дата обращения
    assert "Зозо" == system.get_employee_who_do_task(datetime.date(2024, 2, 3), "ОбТС")
    # Пробуем с СПД. Тут подходят Петров и Зозо, Но у Сидорова много работы (6 тасок), поэтому задача достается Зозо (3 таски).
    assert "Зозо" == system.get_employee_who_do_task(datetime.date(2024, 2, 3), "СПД")
    # А что если дата обращения на отпуск Зозо? Тогда должен быть Петров.
    assert "Петров 2" == system.get_employee_who_do_task(datetime.date(2024, 2, 7), "СПД")
    # Что если нет такого направения? То никого и не будет
    assert "Нет сотрудников для назначения обращения" == system.get_employee_who_do_task(datetime.date(2024, 2, 3),
                                                                                         "ReactJS")
    # А если направление есть, но сотрудники в отпуске? То никого тоже не будет
    assert "Нет сотрудников для назначения обращения" == system.get_employee_who_do_task(datetime.date(2024, 2, 7),
                                                                                         "PhpAdmin")


tech_tests()

# /Users/georgijsilaev/PycharmProjects/testovoe/venv/bin/python /Users/georgijsilaev/PycharmProjects/testovoe/main.py
#
# Process finished with exit code 0