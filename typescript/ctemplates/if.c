{% if expr %}if ({{ expr }}) {% endif %}{
    {{ body }}
} {% if otherwise %}
  else {{ otherwise }}  
{% endif %}
