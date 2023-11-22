import operator

OPERATORS = {'плюс': operator.add, 'минус': operator.sub, 'умножить': operator.mul}

numbers_str_int = {
    'нуль': 0,
    'десять': 10,
    'двадцать': 20,
    'тридцать': 30,
    'сорок': 40,
    'пятьдесят': 50,
    'шестьдесят': 60,
    'семьдесят': 70,
    'восемьдесят': 80,
    'девяносто': 90,
    'один': 1,
    'два': 2,
    'три': 3,
    'четыре': 4,
    'пять': 5,
    'шесть': 6,
    'семь': 7,
    'восемь': 8,
    'девять': 9,
    'одиннадцать': 11,
    'двенадцать': 12,
    'тринадцать': 13,
    'четырнадцать': 14,
    'пятнадцать': 15,
    'шестнадцать': 16,
    'семнадцать': 17,
    'восемнадцать': 18,
    'девятнадцать': 19,
    'сто': 100,
    'двести': 200,
    'триста': 300,
    'четыреста': 400,
    'пятьсот': 500,
    'шестьсот': 600,
    'семьсот': 700,
    'восемьсот': 800,
    'девятьсот': 900,
    'тысяча': 1000
}
numbers_int_str = {numbers_str_int[key]: key for key in numbers_str_int}


def convert_int_to_str(result):
    '''Конвертирует числовой результат в письменный'''
    if result == 0:
        return 'ноль'
    output = ''
    if result < 0:
        output += 'минус '
        result *= -1

    units = result % 10
    tens = result // 10 % 10
    hundreds = result // 100 % 10
    thousands = result // 1000 % 10

    if thousands != 0:
        if thousands == 1:
            output += 'одна тысяча '
        elif thousands in [2, 3, 4]:
            output += numbers_int_str[thousands] + ' тысячи '
        else:
            output += numbers_int_str[thousands] + ' тысяч '
    if hundreds != 0:
        output += numbers_int_str[hundreds * 100] + ' '
    if tens != 0:
        if tens != 1:
            output += numbers_int_str[tens * 10] + ' '
        else:
            prom = 10 + units
            output += numbers_int_str[prom] + ' '
            return output
    if units != 0:
        output += numbers_int_str[units] + ' '
    return output


def do_simple_operation(convert, name_operation):
    '''Находит первые 2 числа, между которомы стоит знак операции == name_operation
    Затем протзводит эту операцию. 2 лишние ячейки удаляются'''
    operation_location = convert.index(name_operation)
    a, b = convert[operation_location - 1], convert[operation_location + 1]
    del convert[operation_location + 1]
    del convert[operation_location]
    convert[operation_location - 1] = OPERATORS[name_operation](a, b)
    return convert


def do_all_operations(convert):
    '''Проводим операцию между рядом стоящими числами
    Сначала выполняется умножение, затем сложение и вычитание по порядку'''
    while 'умножить' in convert:
        convert = do_simple_operation(convert, 'умножить')
    while 'плюс' in convert or 'минус' in convert:
        if 'плюс' in convert and 'минус' in convert:
            plus_location = convert.index('плюс')
            minus_location = convert.index('минус')
            # выполняем операцию, которая идёт раньше
            if plus_location < minus_location:
                convert = do_simple_operation(convert, 'плюс')
            else:
                convert = do_simple_operation(convert, 'минус')
        elif 'плюс' in convert:
            convert = do_simple_operation(convert, 'плюс')
        elif 'минус' in convert:
            convert = do_simple_operation(convert, 'минус')
    return convert


def calculate(s, first_call=True, last_call=True):
    available_operations = ['плюс', 'минус', 'умножить']
    if first_call:
        s = s.replace('умножить на', 'умножить')
        s = s.split()
        convert = []
        # приводим в красивый и удобный виб для работы
        for w in range(len(s)):
            word = s[w]
            if word == 'скобка':
                continue
            elif word == 'открывается':
                convert += ['(']
                continue
            elif word == 'закрывается':
                convert += [')']
                continue
            if word in available_operations:
                convert += [word]
            else:
                # перед нами число
                # если это первое слово в строке - особая обработка
                if w == 0:
                    convert.append(numbers_str_int[word])
                else:
                    if type(convert[-1]) == int:
                        convert[-1] += numbers_str_int[word]
                    else:
                        convert.append(numbers_str_int[word])
        # print(convert)

        # реализация отрицательных чисел
        while 'минус' in convert:
            w = convert.index('минус')
            convert[w] = '-'  # чтобы избежать повторной обработки одного и того же
            if w == 0:
                del convert[0]
                convert[0] *= -1
            else:
                if convert[w - 1] in available_operations + ['-']:
                    del convert[w]
                    convert[w] *= -1
        # возвращаем к прежнему виду
        convert = [i if i != '-' else 'минус' for i in convert]
        # print(convert)
    else:
        convert = s

    while ')' in convert:
        right_bracket_location = convert.index(')')
        # ищем открывающуюся скобочку
        left_bracket_location = right_bracket_location - 1
        while True:
            if convert[left_bracket_location] == '(':
                break
            else:
                left_bracket_location -= 1
        inside = convert[left_bracket_location + 1:right_bracket_location]
        for i in range(len(inside) + 1):
            del convert[left_bracket_location]
        convert[left_bracket_location] = calculate(inside, first_call=False, last_call=')' not in convert)

    convert = do_all_operations(convert)

    if last_call:
        return f'Результат: {convert_int_to_str(convert[0])}'
    else:
        return convert[0]

print(calculate('три умножить на два'))
# print(calculate("скобка открывается пять минус двадцать пять плюс два скобка закрывается умножить три минус один"))
# print(calculate('двадцать пять плюс тринадцать'))
# print(calculate('минус сто двадцать восемь плюс девятьсот сорок четыре'))
# print(calculate("пять минус минус один"))
# print(calculate('тридцать шесть плюс сто двадцать четыре умножить четыре'))
# print(calculate('два плюс два умножить два'))
# print(calculate('скобка открывается два плюс два скобка закрывается умножить два'))
# print(calculate(
#     'скобка открывается два плюс шесть скобка закрывается умножить скобка открывается три плюс шесть скобка закрывается'))
# print(calculate('скобка открывается три плюс четыре умножить на семь скобка закрывается умножить на два'))
# print(calculate('минус два плюс минус четыре минус минус пять'))
# print(calculate('девяносто девять умножить на девяносто девять умножить на девяносто девять минус двести девяносто девять '))

