{% if not definition.parent %}
{{ remap_type(definition.data_type) }} {{ definition.function_name }} ({% for arg in definition.args %}{{ render_definition(arg) if not definition.args_visited else arg }}{% if loop.index < definition.args | length %},{% endif %}{% endfor %}) {
        {{ definition.function_body }}                   
    }
{% else %}
    {{ remap_type(definition.data_type) }} (*{{ definition.function_name }})({% for arg in definition.args %}{{ render_definition(arg) if not definition.args_visited else arg }}{% if loop.index < definition.args | length %},{% endif %}{% endfor %});
{% endif %}
