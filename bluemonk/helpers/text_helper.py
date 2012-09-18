from bluemonk import app
from flask import request, url_for

def to_excerpt(text, length=30):
    if not text:
        return ""
    if len(text) <= length:
        return text

    return "%s ..." % text[:30]

app.jinja_env.filters['to_excerpt'] = to_excerpt
