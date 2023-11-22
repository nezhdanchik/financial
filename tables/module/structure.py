import copy
import csv
import pickle
import datetime
import re
import operator

OPERATORS = {'плюс': operator.add, 'минус': operator.sub, 'умножить': operator.mul}

class Table:
    def __init__(self, count_rows, count_columns, names_of_rows=None, names_of_columns=None):
        self.count_rows = count_rows  # количество строк
        self.count_columns = count_columns  # количество столбцов
        self.names_of_rows = names_of_rows  # список названий строк
        self.names_of_columns = names_of_columns  # список названий столбцов
        self.has_names_of_rows = bool(names_of_rows)
        self.has_names_of_columns = bool(names_of_columns)

        # для типизирования столбцов
        self.column_types = dict()
        self.column_types_by_number = dict()

        self.total_rows = count_rows + 1  # кол-во строк с учётом строки с названием столбцов
        self.total_columns = count_columns + 1  # кол-во столбцов с учётом строки с названием строк

        # создаём нашу таблицу с коррекцией на добавление строк и столбцов для названий
        self.field = [['?' for i in range(count_columns + 1)] for j in range(count_rows + 1)]
        self.field[0][0] = r'Строка\Столбец'

        # задаём имена для столбцов по умолчанию
        for i in range(1, count_columns + 1):
            self.field[0][i] = '№' + str(i)

        # задаём имена для строк по умолчанию
        for i in range(1, count_rows + 1):
            self.field[i][0] = '№' + str(i)

        if names_of_rows:
            if len(names_of_rows) != count_rows:
                raise ValueError(f"Количество названий для строк не совпадает с количеством строк")
            self.set_names_of_rows(names_of_rows)

        if names_of_columns:
            if len(names_of_columns) != count_columns:
                raise ValueError(f"Количество названий для столбцов не совпадает с количеством столбцов")
            self.set_names_of_columns(names_of_columns)

        # задаём типы для столбцов по умолчанию
        for i in range(1, len(self.field[0])):
            self.column_types[self.field[0][i]] = None
            self.column_types_by_number[i] = None

    def create_rows_d(self):
        """делаем словарь для строк. Не знаю зачем тут эта функция"""
        d = dict()
        for row in range(len(self.field)):
            # самая первая строка таблицы содержит названия столбцов
            if row == 0 and self.names_of_columns:
                continue

            if self.names_of_rows:
                d[self.field[row][0]] = self.field[row][1:]

    def set_names_of_rows(self, names_of_rows: list[str]):
        for i in range(1, self.total_rows):
            self.field[i][0] = names_of_rows[i - 1]

    def set_names_of_columns(self, names_of_columns: list):
        for i in range(1, self.total_columns):
            self.field[0][i] = names_of_columns[i - 1]

    def set_one_value(self, value, x, y):
        self.field[y][x] = value

    def set_all_values(self, values: list[list]):
        '''задаём сразу все значения для таблицы'''
        if len(values) != self.count_rows:
            raise ValueError(f"Количество устанавливаемых значений строк не соответствует размеру таблицы")
        if not all(len(i) == self.count_columns for i in values):
            raise ValueError(f"Количество устанавливаемых значений столбцов не соответствует размеру таблицы")
        for i in range(1, self.count_rows + 1):
            self.field[i] = [self.field[i][0]] + values[i - 1]

    @classmethod
    #вспомогательная функция для конвертации матрицы в таблицу
    def convert_matrix_to_table(cls, matrix, has_names_of_rows, has_names_of_columns):
        names_of_rows = []
        names_of_columns = []
        # парсим названия стобцов
        if has_names_of_columns:
            if has_names_of_rows:
                names_of_columns = [matrix[0][i] for i in range(len(matrix[0])) if i != 0]
            else:
                names_of_columns = [i for i in matrix[0]]
            del matrix[0]

        # парсим названия строк
        if has_names_of_rows:
            for i in range(len(matrix)):
                names_of_rows.append(matrix[i][0])
                matrix[i].pop(0)

        t = Table(len(matrix), len(matrix[0]), names_of_rows, names_of_columns)
        t.set_all_values(matrix)
        t.set_column_types(t.define_type(), by_number=False)
        return t

    # -------------------------------------Задание 1-----------------------------------------------

    def _remove_unnecessary_names(self):
        '''удаляет название столбцов или строк, если их не было изначально
        это нужно для правильного сохранения таблицы'''
        result = copy.deepcopy(self.field)
        if not self.has_names_of_columns:
            result.pop(0)
        if not self.has_names_of_rows:
            for i in range(len(result)):
                result[i].pop(0)
        return result

    def save_csv(self, file_name):
        with open(file_name, 'w', newline='') as f:
            csv_witer = csv.writer(f)
            csv_witer.writerows(self._remove_unnecessary_names())

    def save_pickle(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self._remove_unnecessary_names(), f)

    # -----------------------------------Задание 2----------------------------------------------------

    def get_rows_by_number(self, start, stop=None, copy_table=False):
        result = []
        if not stop:
            stop = start
        for i in range(start, stop + 1):
            try:
                result.append(self.field[i])
            except IndexError:
                print('Ошибка: строки с таким номером не существует')
        if copy_table:
            return copy.deepcopy(result)
        return result

    def get_rows_by_index(self, *args, copy_table=False):
        result = []
        for line in self.field:
            if line[1] in args:
                result.append(line)
        if copy_table:
            return copy.deepcopy(result)
        return result

    def get_column_types(self, by_number=True):
        if by_number:
            return self.column_types_by_number
        return self.column_types

    def set_column_types(self, types_dict, by_number=True):
        '''устанавливает типы для столбцов by_number=True -> {number : type}
           by_number=False -> {name_of_column: type}'''
        #здесь мы задаём словарь типов столбцов
        try:
            if by_number:
                new_column_types_by_number = types_dict
                new_column_types = dict()
                #заполняем типы по столбцам по именам
                for i in range(1, len(self.field[0])):
                    new_column_types[self.field[0][i]] = types_dict[i]
            else:
                new_column_types = types_dict
                new_column_types_by_number = dict()
                #заполняем типы по столбцам по индексам
                for key in types_dict:
                    ind = self.field[0].index(key)
                    new_column_types_by_number[ind] = types_dict[key]
        except (ValueError, KeyError):
            print('Ошибка в установлении типов столбцов')
        else:
            self.column_types = new_column_types
            self.column_types_by_number = new_column_types_by_number

        #здесь мы меняем тип у самих значений
        for num_key in self.column_types_by_number:
            t = self.column_types_by_number[num_key]
            #теперь перебираем все элементы в выбранном столбце
            for e in range(1, self.total_rows):
                self.field[e][num_key] = t(self.field[e][num_key])



    def _get_index_column(self, column, error_message):
        """преобразует параметр column в индекс столбца.
        Мы не знаем, на что указывает параметр column (на номер столбца или на название столбца)

        Возвращает сам column, если column это номер столбца, или номер столбца с названием column
        а также тип для этого столбца"""
        try:
            if type(column) == int:
                ind = column
            else:
                ind = self.field[0].index(column)
            t = self.get_column_types(by_number=True)
            t = t[ind] # тип столбца. e.g. int, str, float
            return t, ind
        except (ValueError, KeyError):
            print(error_message)

    def get_values(self, column=0):
        try:
            t, ind = self._get_index_column(column, 'Ошибка в получении значений столбцов: передан неверный параметр')
        except:
            return
        result = []
        for i in range(1, len(self.field)):
            try:
                result.append(t(self.field[i][ind]))
            except TypeError:
                print('Ошибка в получении значений столбцов: типы не были заданы')
                return
        return result


    def get_value(self, column=0):
        try:
            t, ind = self._get_index_column(column, 'Ошибка в получении значений столбцов: передан неверный параметр')
        except:
            return
        try:
            result = t(self.field[1][ind])
            return result
        except TypeError:
            print('Ошибка в получении значений столбцов: типы не были заданы')

    def set_values(self, values, column=0):
        try:
            t, ind = self._get_index_column(column, 'Ошибка в установлении значений столбцов: передан неверный параметр')
        except:
            return
        for i in range(1, len(self.field)):
            try:
                self.field[i][ind] = values[i-1]
            except IndexError:
                print(f'Ошибка в установлении значений столбцов: кол-во элементов столбца != кол-ву элементов  в values')

    def set_value(self,value, column=0):
        try:
            t, ind = self._get_index_column(column, 'Ошибка в установлении значений столбцов: передан неверный параметр')
        except:
            return
        self.field[1][ind] = value


    def print_table(self):
        print()
        new_fielf = copy.deepcopy(self.field)
        # ищем в столбце слово с максимальной длинной
        for x in range(self.total_columns):
            # длина этого слова
            mxlen = max([len(str(self.field[y][x])) for y in range(self.total_rows)])
            # делаем все слова такой же длины + ...
            for y in range(self.total_rows):
                new_fielf[y][x] = str(self.field[y][x]).ljust(mxlen + 4, " ")
        for i in new_fielf:
            print(*i)
        print()

    def define_type(self):
        """Определение типа столбцов по хранящимся в таблице значениям по первому значению
        Возвращает словарь вида {название столбца: определённый тип}"""
        d = dict()
        for i in range(1, len(self.field[0])):
            name_of_column = self.field[0][i]
            elem = self.field[1][i]
            #если это строка, определяем тип
            if type(elem) == str:
                #является ли датой
                #дата должна храниться в формате yyyy-mm-dd
                if re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', elem):
                    d[name_of_column] = datetime.datetime
                elif elem.isdigit():
                    d[name_of_column] = int
                elif elem == 'True' or elem == 'False':
                    d[name_of_column] = bool
                elif elem == 'None':
                    d[name_of_column] = None
                elif elem[0] == '[' and elem[-1] == ']':
                    d[name_of_column] = list
                elif elem[0] == '{' and elem[-1] == '}':
                    d[name_of_column] = dict
                elif elem[0] == '(' and elem[-1] == ')':
                    d[name_of_column] = tuple
                else:
                    d[name_of_column] = str
            #иначе тип уже определён
            else:
                d[name_of_column] = type(elem)
        return d

    def _make_operation_for_columns(self, name1, name2, func_operator):
        """Возвращает список, результатом которого
        является попарное применение operator для элементов столбцов"""
        result = []
        ind1 = self.field[0].index(name1)
        ind2 = self.field[0].index(name2)
        for i in range(1, self.total_rows):
            result.append(func_operator(self.field[i][ind1], self.field[i][ind2]))
        return result

    def add_for_columns(self, name1, name2):
        """Возвращает список, результатом которого
        является попарная сумма элементов столбцов"""
        try:
            return self._make_operation_for_columns(name1, name2, operator.add)
        except TypeError:
            print('Операция сложения невозможна, так как типы элементов столбцов различны')

    def sub_for_columns(self, name1, name2):
        """Возвращает список, результатом которого
        является попарная разность элементов столбцов"""
        try:
            return self._make_operation_for_columns(name1, name2, operator.sub)
        except TypeError:
            print('Операция вычитания невозможна, так как типы элементов столбцов различны')

    def mul_for_columns(self, name1, name2):
        """Возвращает список, результатом которого
        является попарная произведение элементов столбцов"""
        try:
            return self._make_operation_for_columns(name1, name2, operator.mul)
        except TypeError:
            print('Операция умножения невозможна, так как типы элементов столбцов различны')

    def div_for_columns(self, name1, name2):
        """Возвращает список, результатом которого
        является попарное деление элементов столбцов"""
        try:
            return self._make_operation_for_columns(name1, name2, operator.truediv)
        except TypeError:
            print('Операция деления невозможна, так как типы элементов столбцов различны')

    def _make_compare_for_columns(self, name1, name2, func_compare):
        """Возвращает список, результатом которого
        является попарное сравнение элементов столбцов"""
        result = []
        ind1 = self.field[0].index(name1)
        ind2 = self.field[0].index(name2)
        for i in range(1, self.total_rows):
            result.append(func_compare(self.field[i][ind1], self.field[i][ind2]))
        return result

    def eq(self, name1, name2):
        """Возвращает список, результатом которого
        является попарное сравнение элементов столбцов на равенство"""
        try:
            return self._make_compare_for_columns(name1, name2, Compare.eq)
        except TypeError:
            print('Операция сравнения на равенство невозможна, так как типы элементов столбцов различны')

    def gr(self, name1, name2):
        """Возвращает список, результатом которого
        является попарное сравнение элементов столбцов на больше"""
        try:
            return self._make_compare_for_columns(name1, name2, Compare.gr)
        except TypeError:
            print('Операция сравнения на больше невозможна, так как типы элементов столбцов различны')

    def ls(self, name1, name2):
        """Возвращает список, результатом которого
        является попарное сравнение элементов столбцов на меньше"""
        try:
            return self._make_compare_for_columns(name1, name2, Compare.ls)
        except TypeError:
            print('Операция сравнения на меньше невозможна, так как типы элементов столбцов различны')

    def ge(self, name1, name2):
        """Возвращает список, результатом которого
        является попарное сравнение элементов столбцов на больше или равно"""
        try:
            return self._make_compare_for_columns(name1, name2, Compare.ge)
        except TypeError:
            print('Операция сравнения на больше или равно невозможна, так как типы элементов столбцов различны')

    def le(self, name1, name2):
        """Возвращает список, результатом которого
        является попарное сравнение элементов столбцов на меньше или равно"""
        try:
            return self._make_compare_for_columns(name1, name2, Compare.le)
        except TypeError:
            print('Операция сравнения на меньше или равно невозможна, так как типы элементов столбцов различны')

    def ne(self, name1, name2):
        """Возвращает список, результатом которого
        является попарное сравнение элементов столбцов на неравенство"""
        try:
            return self._make_compare_for_columns(name1, name2, Compare.ne)
        except TypeError:
            print('Операция сравнения на неравенство невозможна, так как типы элементов столбцов различны')

    def filter_rows(self, bool_list, copy_table=False):
        result = []
        if len(bool_list) != self.total_rows - 1:
            raise ValueError('Количество элементов bool_list должно быть равно количеству строк в таблице')
        for i in range(1, self.total_rows):
            if bool_list[i - 1]:
                if copy_table:
                    result.append(copy.deepcopy(self.field[i]))
                else:
                    result.append(self.field[i])
        return result

class Compare:
    @staticmethod
    def eq(a, b):
        return a == b
    @staticmethod
    def gr(a, b):
        return a > b
    @staticmethod
    def ls(a, b):
        return a < b
    @staticmethod
    def ge(a, b):
        return a >= b
    @staticmethod
    def le(a, b):
        return a <= b
    @staticmethod
    def ne(a, b):
        return a != b





