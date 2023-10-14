from django import forms

from spaeti.database import username_is_available, email_is_available


# accounts ####################################################################
class AccountAddForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=256,
    )

    email = forms.EmailField(
        label='Email',
    )

    login = forms.BooleanField(
        label='Login',
        required=False,
    )

    spaeti_staff = forms.BooleanField(
        label='Spaeti Staff',
        required=False,
    )

    spaeti_admin = forms.BooleanField(
        label='Spaeti Admin',
        required=False,
    )

    django_staff = forms.BooleanField(
        label='Django Staff',
        required=False,
    )

    django_superuser = forms.BooleanField(
        label='Django Superuser',
        required=False,
    )

    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea,
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username', '')
        email = cleaned_data.get('email', '')

        if username and not username_is_available(username):
            self.add_error('username', 'Username is already taken.')

        if email and not email_is_available(email):
            self.add_error('email', 'Email already taken.')


class AccountEditForm(forms.Form):
    email = forms.EmailField(
        label='Email',
    )

    login = forms.BooleanField(
        label='Login',
        required=False,
    )

    spaeti_staff = forms.BooleanField(
        label='Spaeti Staff',
        required=False,
    )

    spaeti_admin = forms.BooleanField(
        label='Spaeti Admin',
        required=False,
    )

    django_staff = forms.BooleanField(
        label='Django Staff',
        required=False,
    )

    django_superuser = forms.BooleanField(
        label='Django Superuser',
        required=False,
    )

    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea,
        required=False,
    )


class DepositMoneyForm(forms.Form):
    amount = forms.IntegerField(
        label='Amount',
        help_text='Amounts are stored in cents',
    )

    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea,
        required=False,
    )


# products ####################################################################
class ProductAddForm(forms.Form):
    # TODO: check unique fields

    name = forms.CharField(
        label='Name',
        max_length=256,
    )

    slug = forms.CharField(
        label='Slug',
        max_length=256,
        required=False,
    )

    price = forms.IntegerField(
        label='Price',
        help_text='Prices are stored in cents',
    )

    barcode = forms.CharField(
        label='Barcode',
        max_length=256,
        required=False,
    )

    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea,
        required=False,
    )


class ProductEditForm(forms.Form):
    # TODO: check unique fields

    name = forms.CharField(
        label='Name',
        max_length=256,
    )

    slug = forms.CharField(
        label='Slug',
        max_length=256,
        required=False,
    )

    barcode = forms.CharField(
        label='Barcode',
        max_length=256,
        required=False,
    )

    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea,
        required=False,
    )


class ProductRestockForm(forms.Form):
    quantity = forms.IntegerField(
        label='Quantity',
        help_text='Number of products added to the stock',
    )

    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea,
        required=False,
    )


class ProductChangePriceForm(forms.Form):
    price = forms.IntegerField(
        label='Price',
        help_text='Prices are stored in cents',
    )

    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea,
        required=False,
    )
