from lona.html import TBody, Table, Node, Div, Tr, Th, Td
from django.db.models import fields


class DjangoAttributeTable(Div):
    CLASS_LIST = ['django-attribute-table']

    ROWS = [
        # (label: str, column: str | Callable[instance]),
    ]

    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.instance = instance

        # setup html
        self.table_body = TBody()

        self.nodes = [
            Table(
                self.table_body,
            ),
        ]

        self._render()

    def _render(self):
        with self.lock:
            self.table_body.clear()

            for row in self.get_rows():
                label, column = row

                column = self.get_column(
                    instance=self.instance,
                    row=row,
                )

                if not isinstance(label, Node):
                    label = str(label)

                if not isinstance(column, Node):
                    column = str(column)

                self.table_body.append(
                    Tr(
                        Th(label),
                        Td(column),
                    ),
                )

    # entry points ############################################################
    def get_rows(self):
        if self.ROWS:
            return self.ROWS.copy()

        rows = []

        for field in self.instance._meta.fields:
            if isinstance(field, fields.AutoField):
                continue

            if isinstance(field, fields.TextField):
                continue

            rows.append(
                (field.verbose_name, field.name),
            )

        return rows

    def get_column(self, instance, row):
        label, column = row

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

        return column
