import datetime

from typing import List, Dict


# класс Employee, который содержит в себе все основные параметры сотрудника:
class Employee:
    # конструктор
    def __init__(self, num: int, name: str, specs: List[str], tasks_active: int, last_sent_task_date: datetime.date,
                 holidays: List[datetime.date] = None):
        self.num_ = num
        self.name_ = name
        self.spec_ = specs
        self.tasks_active_ = tasks_active
        self.last_sent_task_date_ = last_sent_task_date
        self.holidays_ = holidays

    # Метод проверки, который проверяет наличие передаваемой специальности
    def is_spec_fits(self, spec_on: str):
        if spec_on in self.spec_:
            return True
        return False

    # Метод проверки находится ли сотрудник в отпуске на момент передаваемой даты
    def is_employee_on_vacation(self, task_date: datetime.date):
        if self.holidays_ is None:
            return False
        if self.holidays_[0] <= task_date and self.holidays_[1] >= task_date:
            return True
        return False

    # метод обновления у сторудника даты последнего обращения
    def set_last_sent_task_date(self, task_date: datetime.date):
        self.last_sent_task_date_ = task_date

    # метод обновления текущих обращений
    def set_tasks_active(self, new_tasks: int):
        self.tasks_active_ = new_tasks

    # метод добавления обращения
    def add_task(self):
        self.tasks_active_ += 1


# Основной класс программы-помощника, который хранит в себе словарь с сотрудниками и определяет кому будет назначена
# задача
class EmployeeTaskSystem:
    # Так как в питоне нет нормального объявления двух конструкторов, как в c++/с#, то идем на маленький "костыль"
    # Хотя можно было релиазовать через @dataclass'ы
    def __init__(self, employees: Dict[int, Employee] = None):
        if employees is None:
            employees = {}
        self.e = employees

    # метод добавления сотрудника
    def add_employee(self, employee: Employee):
        self.e[employee.num_] = employee

    # метод получения ID сотрудников, который подходят по специальности.
    def get_employees_id_by_spec(self, spec: str):
        array_of_employees = []
        for employee_id in self.e:
            if self.e[employee_id].is_spec_fits(spec):
                array_of_employees.append(self.e[employee_id].num_)
        return array_of_employees

    def get_employee_with_max_date(self, victims_: List[int]):
        array_of_employees = []
        for id_ in victims_:
            array_of_employees.append(self.e[id_].last_sent_task_date_)

        max_date = min(array_of_employees)  # Берем самую давнюю дату обращения среди подходящих.
        array_of_employees.clear()
        for id_ in victims_:
            # Подходит по максимально удаленной дате? определяем получателя
            if max_date == self.e[id_].last_sent_task_date_:
                return id_
        # если вдруг он всего один и не сработал предыдущий ретерн, то отправляем его одного.
        return array_of_employees[0]

    # Определяем кому достанется обращение. Ожидает на вход: массив ID сотрудников, которые не находятся в отпуске,
    # минимальное значение кол-ва обращений среди подходящих сотрудников и дату обращения
    def decide_who_gets_tasks(self, array_of_ids: List[int], minimum: int, date: datetime.date):
        if len(array_of_ids) >= 2:  # Если сотрудников больше 1, то нам нудно решить кто получает задачу
            victims = []
            for id_ in array_of_ids:
                # Проверяем на наличие минимума задач и даты, которая больше
                if self.e[id_].tasks_active_ == minimum and date > self.e[id_].last_sent_task_date_:
                    victims.append(id_)
            # Что если у нас все идеально и подходит несколько? Берем того, у кого самая дальная дата обращения
            id_victim = self.get_employee_with_max_date(victims)
            # Ну и обновляем у него данные. Ассерты под него не заточены, поэтому закомментим
            # self.e[id_victim].add_task()
            # self.e[id_victim].set_last_sent_task_date(date)
            return self.e[id_victim].name_
        return self.e[array_of_ids[0]].name_  # если только один подходит, то берем его.

    def get_employee_who_do_task(self, date: datetime.date, spec: str):
        # Получаем маассив всех, кто соотвестует направлению
        array_of_employees_this_spec = self.get_employees_id_by_spec(spec)
        if len(array_of_employees_this_spec) == 0:
            # Если никого нет, то увы:
            return "Нет сотрудников для назначения обращения"
        array_of_tasks = []
        array_of_ids_emp = []
        # Здесь мы смотрим кто в отпуске а кто нет. Берем также кол-во их тасок, для нахождения минимума. Добавляем тех, кто не в отпуске
        for i in range(len(array_of_employees_this_spec)):
            if not self.e[array_of_employees_this_spec[i]].is_employee_on_vacation(date):
                array_of_ids_emp.append(array_of_employees_this_spec[i])
                array_of_tasks.append(self.e[array_of_employees_this_spec[i]].tasks_active_)
        if len(array_of_ids_emp) == 0:
            # Если все в отпуске, то увы:
            return "Нет сотрудников для назначения обращения"
        # Отправляем массив подходящих на таску в вспомогательнуб функцию, которая и определит избранного
        return self.decide_who_gets_tasks(array_of_ids_emp, min(array_of_tasks), date)
