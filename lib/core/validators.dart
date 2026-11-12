abstract final class Validators {
  static String? requiredName(String? value) {
    if (value == null || value.trim().isEmpty) return 'Ingresa tu nombre.';
    return null;
  }

  static String? bolivianPhone(String? value) {
    final normalized = (value ?? '').replaceAll(RegExp(r'\s+'), '');
    if (!RegExp(r'^[67]\d{7}$').hasMatch(normalized)) {
      return 'Ingresa un teléfono boliviano válido de 8 dígitos.';
    }
    return null;
  }

  static String? message(String? value) {
    if ((value ?? '').trim().length < 10) {
      return 'El mensaje debe tener al menos 10 caracteres.';
    }
    return null;
  }

  static String? people(String? value) {
    final count = int.tryParse(value ?? '');
    if (count == null || count < 1 || count > 50) {
      return 'Ingresa entre 1 y 50 personas.';
    }
    return null;
  }
}
