from __future__ import unicode_literals

from django.template import Template
from django.template.base import TemplateDoesNotExist, TemplateEncodingError, import_library
from django.template.engine import Engine, _dirs_undefined
from django.template.loaders import app_directories
from django.template.utils import get_app_template_dirs
from django.utils.encoding import force_text

import template_forms.templatetags.forms as form_tags


class FormTemplate(Template):
    def __init__(self, *args, **kwargs):
        engine = kwargs.get('engine', None)
        if engine is None:
            kwargs['engine'] = engine = Engine.get_default()

        # Parse this template with special tags
        engine.use_form_tags = True
        Template.__init__(self, *args, **kwargs)
        engine.use_form_tags = False

        self._enumerate_form_nodes()

    @property
    def _form_nodes(self):
        return self.nodelist.get_nodes_by_type(form_tags.FormNode)

    def _enumerate_form_nodes(self):
        for i, node in enumerate (self._form_nodes):
            node._i = i

    def validate(self, request):
        return all(n.is_valid(request) for n in self._form_nodes)

    def render(self, context):
        context['form_valid'] = self.validate(context.request)

        return Template.render(self, context)


class Loader(app_directories.Loader):
    def load_template(self, template_name, template_dirs=None):
        source, display_name = self.load_template_source(
            template_name, template_dirs)
        origin = self.engine.make_origin(
            display_name, self.load_template_source,
            template_name, template_dirs)

        try:
            # The whole function had to be copy-pasted because of this line
            template = FormTemplate(source, origin, template_name, engine=self.engine)
        except TemplateDoesNotExist:
            return source, display_name
        else:
            return template, None


class FormsEngine(Engine):
    def __init__(self, forms_dir='forms', engine=None):
        if engine is None:
            engine = Engine.get_default()

        self._engine = engine
        self._forms_dirs = get_app_template_dirs(forms_dir)
        self._forms_loader = Loader(self)
        self.use_form_tags = False

        self.context_processors = self._engine.context_processors + ['template_forms.posted_answers']

    def get_template(self, template_name, dirs=_dirs_undefined):
        """
        Returns a compiled Template object for the given template name,
        handling template inheritance recursively.
        """
        if dirs is _dirs_undefined:
            dirs = None
        else:
            warnings.warn(
                "The dirs argument of get_template is deprecated.",
                RemovedInDjango20Warning, stacklevel=2)

        template, origin = self.find_template(template_name, dirs)
        if not hasattr(template, 'render'):
            # template needs to be compiled
            template = FormTemplate(template, origin, template_name, engine=self)
        return template

    def find_form(self, name):
        try:
            source, display_name = self._forms_loader(name, self._forms_dirs)
            origin = self.make_origin(display_name, self._forms_loader, name, self._forms_dirs)
            return source, origin
        except TemplateDoesNotExist:
            raise TemplateDoesNotExist(name)

    def get_form(self, template_name):
        template, origin = self.find_form(template_name)
        if not hasattr(template, 'render'):
            template = FormTemplate(template, origin, template_name, engine=self)
        return template

    def compile_string(self, template_string, origin):
        if self.debug:
            from django.template.debug import DebugLexer, DebugParser
            lexer_class, parser_class = DebugLexer, DebugParser
        else:
            lexer_class, parser_class = Lexer, Parser
        lexer = lexer_class(template_string, origin)
        tokens = lexer.tokenize()
        parser = parser_class(tokens)
        if self.use_form_tags:
#            parser.add_library(import_library('template_forms.templatetags.loader_tags'))
            parser.add_library(import_library('template_forms.templatetags.forms'))
        return parser.parse()

    def __getattr__(self, name):
        return getattr(self._engine, name)


def posted_answers(request):
    answers = request.POST.getlist('gap')
    return {'answers': answers}
