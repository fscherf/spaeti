from lona.html import CheckBox, THead, TBody, Table, Node, Div, Tr, Th, Td, A
from django.db.models import fields


class DjangoTable(Div):
    # TODO: implement pagination
    # TODO: implement selection
    # TODO: implement search
    # TODO: implement filtering

    CLASS_LIST = ['django-table']

    COLUMNS = [
        # (label: str, column: str | Callable[instance]),
    ]

    RIGHT_ALIGNED_COLUMNS = [
        # label: str,
    ]

    def __init__(
        self,
        queryset,
        *args,
        request=None,
        reload_on_filter=False,
        pagination=True,
        selection=False,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)

        self.original_queryset = queryset
        self.request = request
        self.reload_on_filter = reload_on_filter
        self.pagination = pagination
        self.selection = selection

        self.queryset = queryset.all()

        # setup html
        self._right_aligned_column_indexes = (
            self._get_right_aligned_columns_indexes())

        self.table_head = THead()
        self.table_body = TBody()

        self.nodes = [
            Table(
                self.table_head,
                self.table_body,
            ),
        ]

        self._render()

    # rendering ###############################################################
    def _get_right_aligned_columns_indexes(self):
        indexes = []

        for index, (label, _) in enumerate(self.COLUMNS):
            if label in self.RIGHT_ALIGNED_COLUMNS:
                indexes.append(index)

        return indexes

    def _render_table_head(self, columns):
        self.table_head.clear()
        tr = Tr()

        for index, (label, _) in enumerate(columns):
            th = Th(str(label))

            if index in self._right_aligned_column_indexes:
                th.class_list.append('right-aligned')

            tr.append(th)

        if self.selection:
            tr.insert(0, Th(
                CheckBox(),
                _class='select-row',
            ))

        self.table_head.append(tr)

    def _render_table_body(self, columns):
        self.table_body.clear()

        for instance in self.queryset:
            tr = Tr()

            row = self.get_row(
                instance=instance,
                columns=columns,
            )

            show_url = self.get_show_url(instance=instance)

            for index, column in enumerate(row):
                if not isinstance(column, Node):
                    column = str(column)

                if index == 0 and show_url:
                    td = Td(A(column, href=show_url))

                else:
                    td = Td(column)

                if index in self._right_aligned_column_indexes:
                    td.class_list.add('right-aligned')

                tr.append(td)

            if self.selection:
                tr.insert(0, Td(
                    CheckBox(),
                    _class='select-row',
                ))

            self.table_body.append(tr)

    def _render(self):
        columns = self.get_columns()

        with self.lock:
            self._render_table_head(columns=columns)
            self._render_table_body(columns=columns)

    # entry points ############################################################
    def get_columns(self):
        if self.COLUMNS:
            return self.COLUMNS.copy()

        columns = []

        for field in self.original_queryset.model._meta.fields:
            if isinstance(field, fields.AutoField):
                continue

            if isinstance(field, fields.TextField):
                continue

            columns.append(
                (field.verbose_name, field.name),
            )

        return columns

    def get_row(self, instance, columns):
        rows = []

        for label, column in columns:
            if not isinstance(column, str) and not callable(column):
                raise RuntimeError('Columns have to be of type string or callable')

            if isinstance(column, str):
                if hasattr(self, column):
                    column = getattr(self, column)

                elif hasattr(instance, column):
                    column = getattr(instance, column)

                else:
                    raise RuntimeError(f"Neither {instance} nor {self} have an attribute named '{column}'")

            if callable(column):
                column = column(instance)

            rows.append(column)

        return rows

    def get_show_url(self, instance):
        return ''
