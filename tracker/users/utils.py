import re


def has_russian_letters(text):
    """Проверяет, содержит ли строка русские буквы"""
    # Диапазоны русских букв в Unicode:
    # А-я (включая ё и Ё)
    return bool(re.search('[а-яА-ЯёЁ]', text))


def validate_and_format_phone(phone):
    """
    Проверяет и форматирует российский номер телефона.

    Правила:
    1. Убирает все лишние символы (оставляет только цифры и '+' в начале)
    2. Если номер начинается с 8, заменяет на +7
    3. Если номер начинается с 7 (без +), добавляет +
    4. Проверяет, что после кода страны идёт 10 цифр
    5. Возвращает отформатированный номер или False
    """
    # Удаляем всё кроме цифр и плюса
    cleaned = re.sub(r'[^\d+]', '', phone)

    # Проверяем, есть ли плюс не в начале (такое не должно пройти)
    if '+' in cleaned and cleaned.index('+') != 0:
        return False

    # Убираем все плюсы (времено) для удобной обработки
    digits_only = re.sub(r'\+', '', cleaned)

    # Если после удаления всего остались только цифры
    if not digits_only.isdigit():
        return False

    # Проверяем длину "голых" цифр
    if len(digits_only) == 11:
        # Российский номер: 8XXXYYYZZZZ или 7XXXYYYZZZZ
        if digits_only[0] == '8':
            # Заменяем 8 на 7 и добавляем +
            formatted = '+7' + digits_only[1:]
        elif digits_only[0] == '7':
            # Уже начинается с 7, просто добавляем +
            formatted = '+' + digits_only
        else:
            # Начинается с другой цифры
            return False
    elif len(digits_only) == 10:
        # Номер без кода страны (предполагаем, что это РФ)
        formatted = '+7' + digits_only
    else:
        # Неправильная длина
        return False

    # Финальная проверка: должно быть +7 и 10 цифр после (всего 12 символов)
    if re.match(r'^\+7\d{10}$', formatted):
        return formatted
    else:
        return False