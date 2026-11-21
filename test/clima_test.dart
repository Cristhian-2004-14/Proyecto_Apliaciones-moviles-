import 'package:conectacruz/models/clima.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('Clima.fromJson convierte la respuesta actual de Open-Meteo', () {
    final clima = Clima.fromJson({
      'current': {
        'temperature_2m': 28.4,
        'weather_code': 2,
        'time': '2026-11-18T14:00',
      },
    });

    expect(clima.temperatura, 28.4);
    expect(clima.descripcion, 'Parcialmente nublado');
  });
}
