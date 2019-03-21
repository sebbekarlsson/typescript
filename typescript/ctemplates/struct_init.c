init_{{ object_init.class_name }}({% for arg in object_init.args %}{{ arg }}{% endfor %});
{% if backref %}
    {{ backref.data_type.class_name }}_constructor({{ backref.key }}{% if object_init.args %}, {% endif %}{% for arg in object_init.args %}{{ arg }}{% endfor %})
{% endif %}
