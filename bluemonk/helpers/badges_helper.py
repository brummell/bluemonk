from bluemonk import app
from jinja2 import evalcontextfilter, Markup, escape

@evalcontextfilter
def bool_to_badge(eval_ctx, boolean):
    if boolean:
        span = "label-success"
        icon = "icon-ok"
    else:
        span = "label-important"
        icon = "icon-remove"

    template = '<span class="label %s"><i class="%s icon-white"></i></span>'
    out = template % (span, icon)
    if eval_ctx.autoescape:
        out = Markup(out)
    return out

app.jinja_env.filters['bool_to_badge'] = bool_to_badge
