import 'package:flutter_test/flutter_test.dart';

import 'package:conectacruz/models/negocio_configuracion.dart';

void main() {
  test('NegocioConfiguracion interpreta una foto opcional de Supabase', () {
    final config = NegocioConfiguracion.fromMap({
      'id': 'brasas-del-oriente',
      'nombre': 'Brasas del Oriente',
      'foto_path': 'brasas-del-oriente/portada.jpg',
    });

    expect(config.id, 'brasas-del-oriente');
    expect(config.fotoPath, 'brasas-del-oriente/portada.jpg');
  });
}
