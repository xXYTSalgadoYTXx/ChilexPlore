import re
from django.core.exceptions import ValidationError

def validate_password(password):
    """
    Valida que la contraseña cumpla con los siguientes criterios:
    - Al menos 1 número.
    - Al menos 1 carácter en minúscula.
    - Al menos 1 carácter en mayúscula.
    - No debe contener espacios.
    """
    if not re.search(r'[0-9]', password):
        raise ValidationError('La contraseña debe contener al menos un número.')
    if not re.search(r'[a-z]', password):
        raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('La contraseña debe contener al menos una letra mayúscula.')
    if re.search(r'\s', password):
        raise ValidationError('La contraseña no puede contener espacios en blanco.')
    
def validate_telefono(value):
    """
    Valida que el número de teléfono siga un formato válido.
    Este formato permite números con el prefijo '+', números,
    paréntesis, espacios, guiones y puntos.
    """
    # Expresión regular para números de teléfono
    telefono_regex = r'^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    
    if not re.match(telefono_regex, value):
        raise ValidationError(
            f"El número de teléfono '{value}' no es válido. Asegúrate de que sigue el formato adecuado."
        )