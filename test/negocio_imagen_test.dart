import 'package:conectacruz/models/negocio.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('Negocio interpreta la ruta de foto del producto', () {
    final producto = Negocio.fromMap({
      'id': 1,
      'nombre': 'Lomo fino',
      'rubro': 'Cortes',
      'descripcion': 'Corte a la brasa',
      'telefono': '70000000',
      'precio': 84,
      'imagen_path': 'productos/1/foto.jpg',
    });

    expect(producto.imagenPath, 'productos/1/foto.jpg');
  });
}
