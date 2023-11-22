from module.structure import Table
from module.LoadCSV import load_csv
from module.LoadPICKLE import load_pickle


# t = Table(3, 2, names_of_rows=['Даня', 'Петя', 'Вася'], names_of_columns=['Возраст', 'Пол'])
# t.print_table()
# t.set_all_values([['1', '2'], ['3', '4'], ['5', '6']])
# t.print_table()
# t.set_names_of_rows(['Даня', 'Петя', 'Верблюд'])
# t.print_table()


# -----------------------------------------Тест для задания 1-----------------------------------------------------
l1 = load_csv('ovoshi.csv', True, True)
# l2 = load_csv('ovoshi_only_rows.csv', True, False)
# l3 = load_csv('ovoshi_only_columns.csv', False, True)
# l4 = load_csv('ovoshi_nothing.csv', False, False)
# objs = [l1, l2, l3, l4]
# for o in objs:
#     o.print_table()
# l1.save_csv('ovoshi.csv')
# l2.save_csv('ovoshi_only_rows.csv')
# l3.save_csv('ovoshi_only_columns.csv')
# l4.save_csv('ovoshi_nothing.csv')

# p1 = load_pickle('ovoshi.pkl', True, True)
# p2 = load_pickle('ovoshi_only_rows.pkl', True, False)
# p3 = load_pickle('ovoshi_only_columns.pkl', False, True)
# p4 = load_pickle('ovoshi_nothing.pkl', False, False)
# objs = [p1, p2, p3, p4]
# for o in objs:
#     o.print_table()
# p1.save_pickle('ovoshi.pkl')
# p2.save_pickle('ovoshi_only_rows.pkl')
# p3.save_pickle('ovoshi_only_columns.pkl')
# p4.save_pickle('ovoshi_nothing.pkl')

work_obj = l1  #объект, на котором проверяются тесты

# print('---------------------------Тест для  get_rows_by_number------------------------------------------------')
# print('Было:')
# work_obj.print_table()
# # work_obj.set_column_types({1:int, 2:str, 3:int}, by_number=True)
# res = work_obj.get_rows_by_number(1, copy_table=True)
# print(res)
# print('\nСтало:')
# res[0][0] = 'манго'
# print(res)
# work_obj.print_table()
# print('-------------------------------------------------------------------------------------------------------')
#
# print('---------------------------Тест для  get_rows_by_index-------------------------------------------------')
# print('Было:')
# work_obj.print_table()
# res = work_obj.get_rows_by_index(7, 3, copy_table=False)
# print(res)
# print('\nСтало:')
# res[0][0] = 'манго'
# print(res)
# work_obj.print_table()
# print('-------------------------------------------------------------------------------------------------------')
#
#
# print('---------------------------Тест для  get_column_types, set_column_types --------------------------------')
# test1 = Table(2,2,)
# test1.set_all_values([[1,'text'], [23, 'text too']])
# test1.print_table()
# print('Было:')
# print(test1.get_column_types(by_number=False))
# print('\nСтало:')
# test1.set_column_types({2: str, 1: int}, by_number=True)
# print(test1.get_column_types(by_number=False))
# print(test1.get_column_types())
# print('--------------------------------------------------------------------------------------------------------')
# #
# print('---------------------------Тест для  get_values --------------------------------')
# work_obj.print_table()
# work_obj.set_column_types({'вкус':str, 'сытость':int, 'цвет':str}, by_number=False)
# print(work_obj.get_column_types())
# print(work_obj.get_values('вкус'))
# print(work_obj.get_values('сытость'))
# print(work_obj.get_values('цвет'))
# print('---------------------------------------------------------------------------------')
# #
# print('---------------------------Тест для  set_values --------------------------------')
# work_obj.print_table()
# work_obj.set_column_types({1:int, 2:str, 3:int}, by_number=True)
# work_obj.set_values([1,2,3,4], 'сытость')
# work_obj.print_table()
# print('---------------------------------------------------------------------------------')
# #
# print('---------------------------Тест для  set_value и get_value --------------------------------')
# work_obj.print_table()
# work_obj.set_column_types({1:int, 2:str, 3:int}, by_number=True)
# work_obj.set_value('что-то', 'сытость')
# work_obj.print_table()
# print(work_obj.get_value('сытость'), type(work_obj.get_value('сытость')))
# print('---------------------------------------------------------------------------------')
#
#
# print('---------------------------Тест для  define_type--------------------------------')
# work_obj.print_table()
# work_obj.set_column_types(work_obj.define_type(), by_number=False)
# print(work_obj.get_column_types())
# print(work_obj.get_values('цвет'))
# print(work_obj.get_values('вкус'))
# print(work_obj.get_values('сытость'))
# #----------------------- тест для  add_for_columns и mul_for_columns ------------------------
# # print(work_obj.add_for_columns('вкус', 'сытость'))
# # print(work_obj.mul_for_columns('вкус', 'сытость'))
# print(work_obj.eq('вкус', 'сытость'))
# print(work_obj.gr('вкус', 'сытость'))
# print('---------------------------------------------------------------------------------')
# print(work_obj.filter_rows([True, False, True,True], copy_table=False))