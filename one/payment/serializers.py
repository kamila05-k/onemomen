from rest_framework import serializers
import re

class PaymentInputSerializer(serializers.Serializer):
    """
    Сериализатор для ввода данных платежа.
    """
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Введите email.",
            "invalid": "Введите корректный email."
        }
    )
    fio_sender = serializers.CharField(
        required=True,
        max_length=100,
        error_messages={
            "required": "Введите ФИО отправителя.",
            "max_length": "ФИО отправителя не может быть длиннее 100 символов."
        }
    )
    sberbank_card = serializers.CharField(
        required=True,
        max_length=18,
        error_messages={
            "required": "Введите карту Сбербанка.",
            "max_length": "Карта Сбербанка не может быть длиннее 18 символов."
        }
    )
    tether_wallet = serializers.CharField(
        required=True,
        max_length=100,
        error_messages={
            "required": "Введите кошелек Tether (TRC20).",
            "max_length": "Кошелек Tether (TRC20) не может быть длиннее 100 символов."
        }
    )
    payment_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=True,
        error_messages={
            "required": "Введите сумму платежа."
        }
    )
    currency = serializers.CharField(
        required=True,
        max_length=3,
        error_messages={
            "required": "Введите валюту платежа.",
            "max_length": "Валюта платежа не может быть длиннее 3 символов."
        }
    )

    class Meta:
        fields = ["email", "fio_sender", "sberbank_card", "tether_wallet", "payment_amount", "currency"]

    def validate_email(self, value):
        """
        Валидация email, проверяет, что он заканчивается на @example.com.
        """
        if not value.endswith("@example.com"):
            raise serializers.ValidationError("Email должен заканчиваться на @example.com.")
        return value

    def validate_fio_sender(self, value):
        """
        Валидация ФИО отправителя, проверяет, что оно содержит минимум два слова.
        """
        if len(value.split()) < 2:
            raise serializers.ValidationError("ФИО отправителя должно содержать минимум два слова.")
        return value

    def validate_sberbank_card(self, value):
        """
        Валидация карты Сбербанка, проверяет, что она содержит только цифры и длина от 16 до 18 цифр.
        """
        if not re.match(r'^\d{16,18}$', value):
            raise serializers.ValidationError("Карта Сбербанка должна содержать от 16 до 18 цифр.")
        return value

    def validate_tether_wallet(self, value):
        """
        Валидация кошелька Tether (TRC20), проверяет, что длина от 3 до 100 символов.
        """
        if not re.match(r'^[a-zA-Z0-9]{3,100}$', value):
            raise serializers.ValidationError("Кошелек Tether (TRC20) должен содержать от 3 до 100 символов.")
        return value

    def validate_payment_amount(self, value):
        """
        Валидация суммы платежа, проверяет, что сумма больше нуля.
        """
        if value <= 0:
            raise serializers.ValidationError("Сумма платежа должна быть больше нуля.")
        return value

    def validate_currency(self, value):
        """
        Валидация валюты, проверяет, что она состоит из трех букв.
        """
        if not re.match(r'^[A-Z]{3}$', value):
            raise serializers.ValidationError("Валюта должна состоять из трех букв.")
        return value

    def validate(self, attrs):
        """
        Общая валидация всех полей.
        """
        # Здесь можно добавить общую логику валидации, если требуется
        return attrs
