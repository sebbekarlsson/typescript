{% from 'macros/render_arguments.jinja' import render_arguments %}


{% if not definition.parent %}
{{ remap_type(definition.data_type) }} {{ definition.function_name }} ({{ render_arguments(definition.args) }}) {
        {{ definition.function_body }}                   
    }
{% else %}
    {{ remap_type(definition.data_type) }} (*{{ definition.function_name }})({{ 'void' }}* self{% if definition.args %},{% endif %}{{ render_arguments(definition.args) }})
{% endif %}
