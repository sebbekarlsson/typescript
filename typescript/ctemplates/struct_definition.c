{% from 'macros/render_arguments.jinja' import render_arguments %}

typedef struct {{ struct_name.upper() + '_STRUCT' }} {
    {% for definition in definitions %}
        {{ definition }}
    {% endfor %}
} {{ struct_name }};


{% for allocation in allocations %}
    {% if allocation.function_name %}
        {{ remap_type(allocation.data_type) }} {{ struct_name + '_' + allocation.function_name }} ({{ struct_name }}* self{% if allocation.args %},{% endif %}{{ render_arguments(allocation.args) }}) {
        {{ allocation.function_body }}                   
    }
    {% endif %}
{% endfor %}
/**
 * Constructor for {{ struct_name }}
 */
{{ struct_name }}* init_{{ struct_name }}({{ render_arguments(constructor_args) }}) {
    {{ struct_name }}* x = calloc(1, sizeof(struct {{ struct_name.upper() + '_STRUCT' }}));
    {% for allocation in allocations %}
        {% if not allocation.function_name %}
            x->{{ allocation.key }} = calloc(1, sizeof({{ remap_type(allocation.data_type) }}));
        {% endif %}
    {% endfor %}
    return x;
};
