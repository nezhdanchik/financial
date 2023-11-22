import csv
from tables.module.structure import Table

def load_csv(file_name, has_names_of_rows, has_names_of_columns):
    try:
        with open(file_name) as f:
            csv_reader = csv.reader(f)
            loaded_data = []
            for line in csv_reader:
                loaded_data.append(line)
        return Table.convert_matrix_to_table(loaded_data, has_names_of_rows, has_names_of_columns)
    except FileNotFoundError:
        print('Указанный файл не существует')

