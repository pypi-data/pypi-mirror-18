# -*- coding: utf-8 -*-
{{ header }}
{% set classnames = [class_prefix + product_accronym + "Session"] %}{% for filename, classname in filenames.items() %}{%do classnames.append(classname) %}{% endfor %}
__all__ = {{ classnames }}
{% for filename, classname in filenames.items() %}
from .{{ filename }} import {{ classname }}{% endfor %}
from .{{ class_prefix|lower }}{{ product_accronym|lower }}session import {{ class_prefix }}{{ product_accronym }}Session
from .sdkinfo import SDKInfo

def __setup_bambou():
    """ Avoid having bad behavior when using importlib.import_module method
    """
    import pkg_resources
    from bambou import BambouConfig, NURESTModelController

    default_attrs = pkg_resources.resource_filename(__name__, '/resources/attrs_defaults.ini')
    BambouConfig.set_default_values_config_file(default_attrs)

    {% for filename, classname in filenames.iteritems()|sort %}NURESTModelController.register_model({{ classname }})
    {% endfor %}

__setup_bambou()
