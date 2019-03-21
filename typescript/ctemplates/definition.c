{% if definition.parent %}
    {{ remap_type(definition.data_type) }} {{ definition.key }}
{% else %}
    {% if render_data_type %}{{ remap_type(definition.data_type) }} {% endif %}{{ definition.key }}{% if definition.value %}={{ definition.value }}{% endif %}
{% endif %}
