from django import forms
from lona import html

from .static_files import STATIC_FILES


class DjangoForm(html.Form):
    # TODO: make `DJANGO_FORM_CLASS` optional and generate it on the fly
    # if not set

    # TODO: mark required fields better

    STATIC_FILES = STATIC_FILES
    CLASS_LIST = ['django-form']

    FIELD_INPUT_CLASS = 'django-form-input'
    FIELD_ERROR_LIST_CLASS = 'django-form-error-list'
    DJANGO_FORM_CLASS = None
    DJANGO_MODEL_CLASS = None

    def __init__(
            self,
            form_class=None,
            form_data=None,
            model_class=None,
            instance=None,
            handle_save=None,
            handle_save_button_click=None,
            bubble_up=False,
            **kwargs,
    ):

        super().__init__(**kwargs)

        self.django_form_class = form_class or self.DJANGO_FORM_CLASS
        self.django_model_class = model_class or self.DJANGO_MODEL_CLASS
        self.instance = instance
        self.bubble_up = bubble_up

        if handle_save:
            self.handle_save = handle_save

        if handle_save_button_click:
            self.handle_save_button_click = handle_save_button_click

        self.django_form = None
        self.new_instance = None
        self.fields = {}
        self.field_error_lists = {}
        self.field_inputs = {}

        # setup django form
        data = {}

        if instance:
            data.update(forms.model_to_dict(instance))

        if form_data:
            data.update(form_data)

        self.django_form = self.get_django_form_object(data)

        # initial render
        self.render()

    def is_model_form(self):
        return issubclass(self.django_form_class, forms.ModelForm)

    def get_django_form_object(self, data):
        kwargs = {
            'data': data,
        }

        if self.is_model_form() and self.instance is not None:
            kwargs['instance'] = self.instance

        return self.django_form_class(**kwargs)

    @property
    def cleaned_data(self):
        return self.django_form.cleaned_data

    def is_valid(self):
        with self.lock:
            form_data = {}

            for name, field_input in self.field_inputs.items():
                form_data[name] = field_input.value

            self.django_form = self.get_django_form_object(data=form_data)

            self.update_fields()

            return self.django_form.is_valid()

    # rendering ###############################################################
    def render(self):
        with self.lock:
            self.nodes.clear()

            for name, django_field in self.django_form.fields.items():
                field = self.get_field(name)

                self.fields[name] = field

                self.field_error_lists[name] = field.query_selector(
                    f'.{self.FIELD_ERROR_LIST_CLASS}',
                )

                self.field_inputs[name] = field.query_selector(
                    f'.{self.FIELD_INPUT_CLASS}',
                )

                self.nodes.append(field)

    def update_fields(self):
        with self.lock:
            for name in self.fields.keys():
                self.update_field(name)

    # rendering entrypoints ###################################################
    def _get_initial_value(self, name):
        return self.django_form.data.get(
            name,
            self.django_form.fields[name].initial,
        ) or ''

    def get_field_input(self, name):
        # TODO: match field.widget first (choice field vs model choice field)

        django_field = self.django_form.fields[name]

        input_class = None
        input_args = []

        input_kwargs = {
            **django_field.widget.attrs,

            'disabled': django_field.disabled,
            'required': django_field.required,
            'bubble_up': True,
            'class': [self.FIELD_INPUT_CLASS],
            'id': name,
        }

        # CharField
        if isinstance(django_field, forms.CharField):
            if isinstance(django_field.widget, forms.Textarea):
                input_class = html.TextArea

            elif isinstance(django_field.widget, forms.EmailInput):
                input_class = html.TextInput
                input_kwargs['type'] = 'email'

            else:
                input_class = html.TextInput

            # value
            input_kwargs['value'] = self._get_initial_value(name)

            # attributes
            if django_field.min_length:
                input_kwargs['min_length'] = django_field.min_length

            if django_field.max_length:
                input_kwargs['max_length'] = django_field.max_length

        # IntegerField
        elif isinstance(django_field, forms.IntegerField):
            input_class = html.NumberInput

            # value
            input_kwargs['value'] = self._get_initial_value(name)

            # attributes
            if django_field.min_value:
                input_kwargs['min_value'] = django_field.min_value

            if django_field.max_value:
                input_kwargs['max_value'] = django_field.max_value

        # BooleanField
        elif isinstance(django_field, forms.BooleanField):
            input_class = html.CheckBox

            # value
            input_kwargs['value'] = bool(self._get_initial_value(name))

        # Select
        elif isinstance(django_field, forms.ModelChoiceField):
            input_class = html.Select2
            initial_value = self._get_initial_value(name)

            for value, label in django_field.choices:
                if value:
                    value = value.instance

                selected = (value == initial_value or
                            getattr(value, 'pk', None) == initial_value)

                input_args.append(
                    html.Option2(
                        label,
                        value=value,
                        selected=selected,
                    )
                )

        # finalize
        return input_class(*input_args, **input_kwargs)

    def get_field(self, name):
        django_field = self.django_form.fields[name]
        field_input = self.get_field_input(name)

        if isinstance(field_input, html.CheckBox):
            field = html.Label(
                field_input,
                django_field.label or '',
                html.Ul(_class=self.FIELD_ERROR_LIST_CLASS),
            )

        else:
            field = html.Label(
                django_field.label or '',
                html.Ul(_class=self.FIELD_ERROR_LIST_CLASS),
                field_input,
            )

        if django_field.help_text:
            field.insert(1, html.P(django_field.help_text))

        return field

    def update_field(self, name):
        errors = self.django_form.errors.get(name, [])
        error_list = self.field_error_lists[name]
        field_input = self.field_inputs[name]

        # error list
        if error_list:
            error_list.clear()

            for error in errors:
                error_list.append(html.Li(error))

        # input
        if field_input:
            invalid = 'true' if errors else 'false'
            field_input.attributes['aria-invalid'] = invalid

    def set_value(self, field_name, value):
        with self.lock:
            self.field_inputs[field_name].value = value

    def save(self, input_event=None):
        if not self.instance:
            raise RuntimeError('form is not bound')

        if not self.is_valid():
            return

        if self.is_model_form():
            self.django_form.save()

        for field_name, field_input in self.field_inputs.items():
            setattr(self.instance, field_name, field_input.value)

        self.instance.save()
