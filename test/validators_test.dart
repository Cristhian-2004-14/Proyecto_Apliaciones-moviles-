import 'package:conectacruz/core/validators.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Validators', () {
    test('acepta teléfono boliviano de ocho dígitos que inicia en 6 o 7', () {
      expect(Validators.bolivianPhone('71234567'), isNull);
      expect(Validators.bolivianPhone('61234567'), isNull);
    });

    test('rechaza teléfonos y reservas fuera de rango', () {
      expect(Validators.bolivianPhone('51234567'), isNotNull);
      expect(Validators.people('0'), isNotNull);
      expect(Validators.people('51'), isNotNull);
      expect(Validators.people('4'), isNull);
    });
  });
}
