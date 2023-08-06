import pattern.text.en as pattern

import data.types as gen_types
import template.controller as controller_file_gen
import template.model.model as model_file_gen
import template.repository as repo_file_gen
import template.service as service_file_gen
from domain.file_information import FileInformation
from util.util import *

_generation_map = {
    'scaffold': [
        gen_types.MODEL,
        gen_types.REPOSITORY,
        gen_types.SERVICE,
        gen_types.CONTROLLER,
    ]
}

_template_map = {
    gen_types.MODEL: model_file_gen,
    gen_types.REPOSITORY: repo_file_gen,
    gen_types.SERVICE: service_file_gen,
    gen_types.CONTROLLER: controller_file_gen,
}


def generate_file(file_info):
    template = _template_map[file_info.file_type]

    file_contents = template.gen_contents(file_info)
    create_file(file_info.file_path, file_info.file_name, file_contents)


def perform(gen_type, gen_name, fields):
    generations = _generation_map[gen_type]

    if not (gen_name and gen_type):
        return "Missing required argument"
    if not generations:
        return "Unknown generation type :", gen_type

    gen_name = pattern.singularize(gen_name.capitalize().replace(' ', ''))
    files_to_generate = [FileInformation(gen_name, fields, elem) for elem in generations]
    for file_to_generate in files_to_generate:
        generate_file(file_to_generate)
