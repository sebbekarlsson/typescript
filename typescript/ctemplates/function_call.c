{{ function_name }}({% for arg in args %}{{ arg }}{% if loop.index < args | length %},{% endif %}{% endfor %})
