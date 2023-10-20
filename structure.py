import copy
from copy import deepcopy
import csv
import pickle


class Table:
    def __init__(self, count_rows, count_columns, names_of_rows=None, names_of_columns=None, values=None, ):
        self.count_rows = count_rows  # количество строк
        self.count_columns = count_columns  # количество столбцов
        self.names_of_rows = names_of_rows
        self.names_of_columns = names_of_columns
        self.has_names_of_rows = bool(names_of_rows)
        self.has_names_of_columns = bool(names_of_columns)
        self.values = values #значения без названий строк и столбцов
        # self.rows_d = None  # словарь  строк
        # self.columns_d = None  # cловарь столбцов

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

    def create_rows_d(self):
        '''делаем словарь для строк'''
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
    def _convert_matrix_to_table(cls, matrix, has_names_of_rows, has_names_of_columns):
        # print(matrix, type(matrix), has_names_of_rows, has_names_of_columns)
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
        return t

    # -------------------------------------Задание 1-----------------------------------------------
    @classmethod
    def load_csv(cls, file_name, has_names_of_rows, has_names_of_columns):
        with open(file_name) as f:
            csv_reader = csv.reader(f)
            loaded_data = []
            for line in csv_reader:
                loaded_data.append(line)
        return cls._convert_matrix_to_table(loaded_data, has_names_of_rows, has_names_of_columns)


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

    @classmethod
    def load_pickle(cls, file_name, has_names_of_rows, has_names_of_columns):
        with open(file_name, 'rb') as f:
            loaded_data = pickle.load(f)
        return cls._convert_matrix_to_table(loaded_data, has_names_of_rows, has_names_of_columns)

    def save_pickle(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self.field, f)

    # -----------------------------------Задание 2----------------------------------------------------

    def get_rows_by_number(self, start, stop=None, copy_table=False):
        result = []
        if not stop:
            stop = start
        for i in range(start, stop + 1):
            result.append(self.field[i])
        if copy_table:
            return copy.deepcopy(result)
        return result

    def get_rows_by_index(self, *args, copy_table=False):
        result = []
        for line in self.field:
            if line[1] in args:
                result.append(line)
        return result

    def get_column_types(self, by_number=True):
        pass

    def set_column_types(self, types_dict, by_number=True):
        pass

    def get_values(column=0):
        pass

    def get_value(column=0):
        pass

    def set_values(values, column=0):
        pass

    def set_value(column=0):
        pass

    def print_table(self):
        new_fielf = deepcopy(self.field)
        # ищем в столбце слово с максимальной длинной
        for x in range(self.total_columns):
            # длина этого слова
            mxlen = max([len(self.field[y][x]) for y in range(self.total_rows)])
            # делаем все слова такой же длины + ...
            for y in range(self.total_rows):
                new_fielf[y][x] = self.field[y][x].ljust(mxlen + 4, " ")
        for i in new_fielf:
            print(*i)


# t = Table(3, 2, names_of_rows=['Даня', 'Петя', 'Вася'], names_of_columns=['Возраст', 'Пол'])
# t.print_table()
# t.set_all_values([['1', '2'], ['3', '4'], ['5', '6']])
# t.print_table()
# t.set_names_of_rows(['Даня', 'Петя', 'Верблюд'])
# t.print_table()

# t = Table.load_pickle('testpickle.pkl', True, True)


# -----------------------------------------Тест для задания 1-----------------------------------------------------
l1 = Table.load_csv('ovoshi.csv', True, True)
l2 = Table.load_csv('ovoshi_only_rows.csv', True, False)
l3 = Table.load_csv('ovoshi_only_columns.csv', False, True)
l4 = Table.load_csv('ovoshi_nothing.csv', False, False)
objs = [l1, l2, l3, l4]
for o in objs:
    o.print_table()
# l1.save_csv('ovoshi.csv')
# l2.save_csv('ovoshi_only_rows.csv')
# l3.save_csv('ovoshi_only_columns.csv')
# l4.save_csv('ovoshi_nothing.csv')

# l4.set_one_value('5', 1, 1)
# l3.print_table()
# l3.save_csv('ovoshebasa_only_columns.csv')

# print('---------------------------Тест для  get_rows_by_number------------------------------------------------')
# t = Table.load_csv('ovoshebasa.csv', ';',True, True)
# t.print_table()
# t1 = t.get_rows_by_number(1, copy_table=False)
# print(t1)
# t1[0][0] = 'манго'
# print(t1)
# t.print_table()
# print('-------------------------------------------------------------------------------------------------------')

# print('---------------------------Тест для  get_rows_by_index------------------------------------------------')
# t = Table.load_csv('ovoshebasa.csv', ';',True, True)
# t.print_table()
# t1 = t.get_rows_by_index('7')
# print(t1)
# t1[0][0] = 'манго'
# print(t1)
# t.print_table()
# print('-------------------------------------------------------------------------------------------------------')

# p.print_table()
# p.get_rows_by_number(1)

# # t.save_pickle('testpickle.pkl')
# Table.load_pickle('testpickle.pkl')
