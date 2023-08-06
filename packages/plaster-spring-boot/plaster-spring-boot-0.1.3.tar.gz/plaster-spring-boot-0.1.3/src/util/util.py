import os
import re


def create_file(path, name, file_contents, create_not_found_dirs=True, mode="w+"):
    if create_not_found_dirs and not os.path.isdir(path):
        os.makedirs(path)

    file = open(os.path.join(path, name), mode)
    file.write(file_contents)
    file.close()


def type_to_var(type):
    return type[0].lower() + type[1:]


def type_to_snake_case(type):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', type)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
