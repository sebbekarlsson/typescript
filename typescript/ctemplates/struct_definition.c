typedef struct {{ struct_name.upper() + '_STRUCT' }} {
    {% for definition in definitions %}
        {{ definition }}
    {% endfor %}
} {{ struct_name }};


/**
 * Constructor for {{ struct_name }}
 */
{{ struct_name }}* init_{{ struct_name }}() {
    {{ struct_name }}* x = calloc(1, sizeof(struct {{ struct_name.upper() + '_STRUCT' }}));
    return x;
};
