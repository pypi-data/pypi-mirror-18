import template.template_util as template_util

_template = """package {package};

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.data.repository.CrudRepository;

import {model_package}.{model};

public interface {class_name} extends CrudRepository<{model}, {id_type}> {{

    Page<{model}> findAll(Specification<{model}> spec, Pageable pageInfo);

    {model} findOne(Specification<{model}> spec);


}}
"""


def gen_contents(file_info, id_type='Integer'):
    return template_util.format_template(_template.format(
        package=file_info.package,
        class_name=file_info.class_name,
        model_package=file_info.model_package,
        model=file_info.model_name,
        id_type=id_type))
