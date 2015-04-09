from __future__ import unicode_literals

from functools import partial
from django import template
from django.template import Node
from django.utils.html import format_html

register = template.Library()


class FormNode(Node):
    def __init__(self):
        self._i = None

    def is_valid(self, context):
        """
        Check that the data is valid.
        """
        return True


class GapFormNode(FormNode):
    def __init__(self, answers, case_sensitive=False):
        if not answers:
            raise template.TemplateSyntaxError('The gap must have at least one valid answer')

        self._case_sensitive = case_sensitive
        self._answers = answers

        if not case_sensitive:
            self._answers = [a.lower() for a in answers]

        FormNode.__init__(self)

    def _posted_answer(self, context):
        gaps = context.get('answers', None)
        if not gaps:
            return ''
        try:
            gap = gaps[self._i]
        except IndexError:
            return ''
        return gap

    def is_valid(self, context):
        ans = self._posted_answer(context)
        if not ans:
            return None

        if not self._case_sensitive:
            ans = ans.lower()
        return ans in self._answers

    def render(self, context):
        valid = self.is_valid(context)

        return format_html('<input type="text" name="gap" value="{ans}" class="form-control input-sm gap {validity_class}">',
                           ans=self._posted_answer(context),
                           validity_class='' if valid is None else 'gap-valid' if valid else 'gap-invalid',
                          )

@register.tag
def gap(parser, token, case_sensitive=False):
    try:
        tag_name, data = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a list of valid answers" % token.contents.split()[0]
        )
    answers = list(filter(bool, [s.strip() for s in data.split('|')]))
    return GapFormNode(answers, case_sensitive)

register.tag('gap_case', partial(gap, case_sensitive=True))
