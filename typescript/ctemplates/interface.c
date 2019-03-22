typedef struct {{ interface_name }}_STRUCT {
    {% for definition in definitions %}
        {{ definition }};
    {% endfor %}
}{{ interface_name }}
