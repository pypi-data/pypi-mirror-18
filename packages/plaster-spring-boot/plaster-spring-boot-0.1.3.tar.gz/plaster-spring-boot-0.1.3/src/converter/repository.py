import pattern.text.en as pattern

import data.settings as settings
from data.types import REPOSITORY as GEN_TYPE


def gen_package_name():
    return settings.MAVEN_GROUP_ID + '.' + settings.RELATIVE_PACKAGES[GEN_TYPE]


def gen_class_name(root_name):
    return pattern.singularize(root_name) + 'Repository'


def gen_file_path():
    return settings.REL_PATH + settings.RELATIVE_PACKAGES[GEN_TYPE]


def gen_file_name(root_name):
    return gen_class_name(root_name) + '.java'
