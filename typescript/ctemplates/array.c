{ {% for item in items %}{{ item }}{% if loop.index < items | length %},{% endif %}{% endfor %}  }
