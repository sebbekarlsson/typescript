{% from 'macros/render_definition.jinja' import render_definition %}
{% from 'macros/render_function_definition.jinja' import render_function_definition %}


typedef struct {{ struct_name.upper() + '_STRUCT' }} {
    {% for definition in definitions %}
        {% if not definition.function_name %}
            {{ render_definition(definition) }};
        {% else %}
            {{ remap_type(definition.data_type) }} (*{{ definition.function_name }})({% for arg in definition.args %}{{ render_definition(arg) }}{% endfor %});
        {% endif %}
    {% endfor %}
} {{ struct_name }};


{% for definition in definitions %}
    {% if definition.function_name %}
        {{ render_function_definition(definition, struct_name + '_') }}
    {% endif %}
{% endfor %}

/**
 * Constructor for {{ struct_name }}
 */
{{ struct_name }}* init_{{ struct_name }}() {
    {{ struct_name }}* x = calloc(1, sizeof(struct {{ struct_name.upper() + '_STRUCT' }}));
    {% for definition in definitions %}
        {% if not definition.function_name %}
            x->{{ definition.key }} = calloc(1, sizeof({{ remap_type(definition.data_type) }}));
        {% else %}
            x->{{ definition.function_name }} = {{ struct_name }}_{{ definition.function_name }};
        {% endif %}
    {% endfor %}
    return x;
};
