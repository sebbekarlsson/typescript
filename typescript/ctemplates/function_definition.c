{{ data_type or 'void' }} {{ function_name }} ({% for arg in args %}{{ arg }}{% if loop.index < args | length %},{% endif %}{% endfor %}) {
    {{ function_body }}                   
}
