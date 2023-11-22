import pickle
from tables.module.structure import Table
def load_pickle(file_name, has_names_of_rows, has_names_of_columns):
    try:
        with open(file_name, 'rb') as f:
            loaded_data = pickle.load(f)
        return Table.convert_matrix_to_table(loaded_data, has_names_of_rows, has_names_of_columns)
    except FileNotFoundError:
        print('Указанный файл не существует')