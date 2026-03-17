import re


def has_russian_letters(text):
    """Проверяет, содержит ли строка русские буквы"""
    # Диапазоны русских букв в Unicode:
    # А-я (включая ё и Ё)
    return bool(re.search('[а-яА-ЯёЁ]', text))

def validate_phone_number(phone):
    cleaned = re.sub(r'[^\d+]', '', phone)
    if len(cleaned) < 12 or len(cleaned) > 16:
        return False
    else:
        if len(cleaned) < 10 or len(cleaned) > 15:
            return False

    return True