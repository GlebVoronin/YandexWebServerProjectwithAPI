from wtforms.validators import StopValidation


class CheckStringFieldByDigit(object):
    field_flags = ('digit_check',)

    @staticmethod
    def check_string_by_digits_and_symbols(string):
        """
        Проверка строки на нормальный вид дробного числа, кратного 0.1
        Используется при вводе пользователем длины ткани при оформлении заказа
        """
        string = str(string).strip()
        if not string:
            return False
        elif string.count('.') > 1 or string.count(',') > 1:
            return False
        for symbol in ['.', ',']:  # возможные разделители дробных чисел
            if symbol in string:
                if not string.replace(symbol, '0').isdigit():
                    return False
                elif len(string.split(symbol)[1]) > 1:
                    return False
        return True

    def __call__(self, form, field):
        if not self.check_string_by_digits_and_symbols(field.data):
            message = field.gettext('Вы ввели неправильное значение')
            field.errors[:] = []
            raise StopValidation(message)
