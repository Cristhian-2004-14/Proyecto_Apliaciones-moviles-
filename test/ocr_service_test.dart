import 'package:flutter_test/flutter_test.dart';

import 'package:conectacruz/services/ocr_service.dart';

void main() {
  final service = OcrService();

  test('extrae los campos principales de un comprobante BMSC válido', () {
    final result = service.parseText('''
      Mercantil Santa Cruz
      ¡Transferencia exitosa!
      Fecha: 17/11/2026
      Importe: Bs. 69,50
      CUENTA DESTINO
      Beneficiario de prueba
      0000-123456
      Código de operación: ABC-12345
    ''');

    expect(result.banco, 'Banco Mercantil Santa Cruz');
    expect(result.exitoso, isTrue);
    expect(result.monto, 69.50);
    expect(result.fechaOperacion, DateTime(2026, 11, 17));
    expect(result.codigoOperacion, 'ABC-12345');
  });

  test(
    'deja campos vacíos cuando el comprobante es ilegible o de otro banco',
    () {
      final result = service.parseText(
        'Comprobante sin datos bancarios verificables',
      );

      expect(result.banco, isNull);
      expect(result.monto, isNull);
      expect(result.exitoso, isNull);
      expect(result.tieneDatosBasicos, isFalse);
    },
  );

  test('admite fecha textual y normaliza el monto', () {
    final result = service.parseText('''
      Banco Mercantil Santa Cruz
      Operación exitosa
      Monto Bs 1.250,00
      17 de noviembre de 2026
    ''');

    expect(result.monto, 1250.00);
    expect(result.fechaOperacion, DateTime(2026, 11, 17));
  });
}
