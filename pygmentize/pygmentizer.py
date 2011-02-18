import re
from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter
from django.http import HttpResponse
from pygments.lexers import HtmlLexer
import settings

#add code number lines(taken from https://github.com/odeoncg/django-pygments.git)
class ListHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        return self._wrap_div(self._wrap_pre(self._wrap_list(source)))

    def _wrap_list(self, source):
        yield 0, '<ol>'
        for i, t in source:
            if i == 1:
                # it's a line of formatted code
                t = '<li><div class="line">%s</div></li>' % t
            yield i, t
        yield 0, '</ol>'

def add_pygment(matchobj):
    #string = matchobj.group(0)
    lang = matchobj.group(2)
    text = matchobj.group(4)
    #print text, lang
    try:
        lexer = get_lexer_by_name(lang, encoding='UTF-8')
    except:
        lexer = HtmlLexer()
    return highlight(text, lexer, ListHtmlFormatter(encoding='utf-8'))

""" look for {% pygmentize 'language' %} tags """
def pygmentize(text):
    #print "trying to pygmentize", text
    return re.sub(r'(?s)\{\%\ *pygmentize\ *(\'|\")([a-zA-Z0-9\+\-]*)(\'|\")\ *\%\}(.*?)\{\%\ *endpygmentize\ *\%\}', lambda x: add_pygment(x), text)

 
def get_css(request):
    style = getattr(settings, "PYGMENT_THEME", "native")
    return HttpResponse(unicode(HtmlFormatter(style=style).get_style_defs('.highlight')), mimetype="text/css")



