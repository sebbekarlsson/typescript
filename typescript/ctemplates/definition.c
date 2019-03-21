{% if definition.parent %}
    {{ remap_type(definition.data_type) }} {{ definition.key }};
{% else %}
    {{ remap_type(definition.data_type) }} {{ definition.key }}{% if definition.value %}={{ definition.value }}{% endif %}
{% endif %}
