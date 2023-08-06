import converter.model as model_converter
import converter.repository as repo_converter
import template.template_util as template_util
import util.util as util

_template = """package {package};

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import {model_package}.{model_class};
import {repo_package}.{repo_class};

@Service
public class {class_name} {{

    private final {repo_class} {repo_var};

    @Autowired
    public {class_name}({repo_class} {repo_var}) {{
        this.{repo_var} = {repo_var};
    }}

    public {model_class} create({model_class} {model_var}) {{
        return this.{repo_var}.save({model_var});
    }}

    public {model_class} read({id_type} id) {{
        return this.{repo_var}.findOne(id);
    }}

    public {model_class} update({model_class} {model_var}) {{
        return this.{repo_var}.save({model_var});
    }}

    public void delete({id_type} id) {{
        this.{repo_var}.delete(id);
    }}

}}

"""


def gen_contents(file_info, id_type='Integer'):
    repo_package = repo_converter.gen_package_name()
    repo_class = repo_converter.gen_class_name(file_info.seed_name)
    model_package = model_converter.gen_package_name()
    model_class = model_converter.gen_class_name(file_info.seed_name)

    return template_util.format_template(_template.format(
        package=file_info.package,
        class_name=file_info.class_name,
        model_package=model_package,
        model_class=model_class,
        model_var=util.type_to_var(model_class),
        repo_class=repo_class,
        repo_package=repo_package,
        repo_var=util.type_to_var(repo_class),
        id_type=id_type))
