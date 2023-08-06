from actions import ActionsMixin
from flask import flash, request
from flask import redirect
from flask_admin.actions import action
from flask_admin.babel import lazy_gettext, ngettext, gettext
from flask_admin.base import AdminIndexView
from flask_admin.contrib.sqla import tools
from flask_admin.contrib import sqla
from form import ModelConverter, InlineModelConverter
from shelf.security.mixin import LoginMixin
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

class IndexView(LoginMixin, AdminIndexView):
    def __init__(self, name=None, category=None,
                 endpoint=None, url=None,
                 template='admin/index.html'):
        super(IndexView, self).__init__(name,
                                        category,
                                        endpoint or 'admin',
                                        url or '/admin',
                                        'static')
        self._template = template

class SQLAModelView(LoginMixin, sqla.ModelView, ActionsMixin):
    list_template = "shelf/model/list.html"
    create_template = "shelf/model/create.html"
    edit_template = "shelf/model/edit.html"

    form_overrides = None
    form_args = None
    sort_overrides = None

    model_form_converter = ModelConverter
    inline_model_form_converter = InlineModelConverter

    def __init__(self, *args, **kwargs):
        if self.form_overrides is None:
            self.form_overrides = dict()
        if self.form_args is None:
            self.form_args = dict()
        if self.sort_overrides is None:
            self.sort_overrides = dict()

        super(SQLAModelView, self).__init__(*args, **kwargs)
        self.extensions = {}

        self.form_shortcuts = getattr(self, 'form_shortcuts', tuple())

    def get_column_name(self, field):
        """
            Return a human-readable column name.
            :param field:
                Model field name.
        """
        if self.column_labels and field in self.column_labels:
            return self.column_labels[field]
        else:
            if hasattr(self.model, field):
                model_field = getattr(self.model, field)
                if hasattr(model_field, 'info') and 'label' in model_field.info and model_field.info['label']:
                    return "%s%s" % (model_field.info['label'][:1].upper(), model_field.info['label'][1:])
            return self._prettify_name(field)

    def prettify_name(self, field):
        return self.get_column_name(field)

    def scaffold_sortable_columns(self):
        columns = sqla.ModelView.scaffold_sortable_columns(self)
        if hasattr(self, "sort_overrides"):
            for k, v in self.model.__dict__.items():
                if hasattr(v, "mapper"):
                    cls = v.mapper.class_
                    for mixin in self.sort_overrides:
                        if issubclass(cls, mixin) and k not in columns:
                            columns[k] = v
        return columns

    def _order_by(self, query, joins, sort_joins, sort_field, sort_desc):
        if hasattr(sort_field, "mapper"):
            for mixin in self.sort_overrides:
                if issubclass(sort_field.mapper.class_, mixin):
                    return self.sort_overrides[mixin](query, joins, sort_joins, sort_field, sort_desc)
        query, joins = sqla.ModelView._order_by(self, query, joins, sort_joins, sort_field, sort_desc)
        return query, joins

    def extend_view(self, endpoint, block, template):
        if endpoint not in self.extensions:
            self.extensions[endpoint] = {}
        if block not in self.extensions[endpoint]:
            self.extensions[endpoint][block] = []
        self.extensions[endpoint][block].append(template)

    def extend_form(self, key, field, args):
        self.form_overrides[key] = field
        self.form_args[key] = args

    def extend_sort(self, cls, fct):
        self.sort_overrides[cls] = fct

    def additionnal_context(self):
        view, method = request.endpoint.split('.')
        extensions = {}
        for view_name in (request.endpoint,
                "modelview.{}".format(method)):
            if view_name in self.extensions:
                view_extensions = self.extensions[view_name]
                for block in view_extensions:
                    if block not in extensions:
                        extensions[block] = []
                    for template in view_extensions[block]:
                        extensions[block].append(template)

        return {
            "views_extensions": extensions
        }

    def create_blueprint(self, admin):
        bp = super(SQLAModelView, self).create_blueprint(admin)
        @bp.context_processor
        def add_user_panel():
            return self.additionnal_context()
        return bp

    # Default model actions
    def is_action_allowed(self, name):
        # Check delete action permission
        if name == 'export_all' and not self.can_export:
            return False

        return super(SQLAModelView, self).is_action_allowed(name)

    @action('export_all', lazy_gettext("Export all"))
    def action_export(self, ids, query):
        return redirect(self.get_url('.export_csv'))

    @action('delete',
            lazy_gettext('Delete'),
            lazy_gettext('Are you sure you want to delete selected models?'))
    def action_delete(self, ids, query):
        try:
            if self.fast_mass_delete:
                count = query.delete(synchronize_session=False)
            else:
                count = 0

                for m in query.all():
                    self.session.delete(m)
                    count += 1

            self.session.commit()

            flash(ngettext('Model was successfully deleted.',
                           '%(count)s models were successfully deleted.',
                           count,
                           count=count))
        except Exception as ex:
            if self._debug:
                raise

            flash(gettext('Failed to delete models. %(error)s', error=str(ex)), 'error')
