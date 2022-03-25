from django import forms
from .models import DelieveryOption, DelieveryCityOption, PaymentOption

CITIES_OPTIONS = (
    ('BL', 'Бельцы'),
    ('С', 'Кишинев'),
    ('CH', 'Кагул'),
    ('TP', 'Тирасполь'),
    ('CD', 'Чадыр-Лунга'),
    ('ED', 'Единцы'),
)

PAYMENT_OPTIONS = (
    ('D', 'Оплата при доставке'),
    ('CR', 'Рассчитать в кредит'),
)

DELIEVERY_OPTIONS = (
    ('DM', 'Доставка по всей молдове'),
    ('DB', 'Доставка по Бельцам'),
    ('MS', 'Заберу сам | Ул. Киевская 128'),
)


class CheckoutForm(forms.Form):
    customer_first_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        'placeholder': 'Ваня',
        'class': "form-control",
        'aria-label': "Ваня",
        'required': "",
        'data-msg': "Пожалуйста, введите Ваше имя.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
    }))
    last_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        'placeholder': 'Иванов',
        'class': "form-control",
        'aria-label': "Иванов",
        'required': "",
        'data-msg': "Пожалуйста, введите Вашу фамилию.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
    }))
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'strada Stefan cel Mare, 21',
        'class': "form-control",
        'aria-label': "strada Stefan cel Mare, 21",
        'required': "",
        'data-msg': "Пожалуйста, введите коректный адрес.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
    }))
    city_address = forms.ModelChoiceField(queryset=DelieveryCityOption.objects.all(), widget=forms.Select(attrs={
        'placeholder': 'Бельцы',
        'class': "form-control",
        'aria-label': "Бельцы",
        'required': "",
        'data-msg': "Пожалуйста, введите коректный адрес.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
        'autocomplete': "off",
    }))
    postcode = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'MD-3100',
        'class': "form-control",
        'aria-label': "MD-3100",
        'required': "",
        'data-msg': "Пожалуйста, введите почтовый индекс.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'ivanivanov@mail.ru',
        'class': "form-control",
        'aria-label': "ivanivanov@mail.ru",
        'required': "",
        'data-msg': "Пожалуйста, введите Ваш корректный E-mail",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '+373 69 99 9999',
        'class': "form-control",
        'aria-label': "+373 69 99 9999",
        'data-success-class': "u-has-success",
    }))
    create_an_account = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': "custom-control-input",
        'id': "createAnaccount",
        'data-success-class': "u-has-success",
    }))
    sign_in_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'placeholder': '********',
        'class': "form-control",
        'id': "signinSrPasswordExample1",
        'aria-label': "********",
        'data-msg': "Пожалуйста, введите пароль",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
        'required': "",
    }))
    terms_and_conditions = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': "form-check-input",
            'id': "defaultCheck10",
            'required': "",
        }))


class LeaveTheMessageForm(forms.Form):
    first_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={
        'placeholder': 'Иван',
        'class': "form-control",
        'aria-label': "Иван",
        'required': "",
        'data-msg': "Пожалуйста, введите Ваше имя.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
        'autocomplete': "off",
    }))
    last_name = forms.CharField(max_length=25, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Иванов',
        'class': "form-control",
        'aria-label': "Иванов",
        'data-msg': "Пожалуйста, введите Вашу фамилию.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
    }))
    email = forms.EmailField(max_length=55, widget=forms.TextInput(attrs={
        'placeholder': 'my@email.com',
        'class': "form-control",
        'aria-label': "Иванов",
        'required': "",
        'data-msg': "Пожалуйста, введите Вашу фамилию.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
    }))
    subject = forms.CharField(max_length=155, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Мне нужна помощь',
        'class': "form-control",
        'aria-label': "Тема сообщения",
        'data-msg': "Пожалуйста, введите тему сообщения.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Пожалуйста, подскажите ...',
        'class': "form-control",
        'aria-label': "Сообщение",
        'required': "",
        'data-msg': "Пожалуйста, введите тему сообщения.",
        'data-error-class': "u-has-error",
        'data-success-class': "u-has-success",
    }))
