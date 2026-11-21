import 'package:conectacruz/models/negocio.dart';
import 'package:conectacruz/services/carrito_controller.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  const producto = Negocio(
    id: 1,
    nombre: 'Parrillada Oriente',
    rubro: 'Parrilladas',
    descripcion: 'Prueba',
    telefono: '70000000',
    precio: 98,
    icono: Icons.outdoor_grill,
  );

  test('el carrito suma cantidades y total del producto', () {
    final carrito = CarritoController();
    carrito.agregar(producto);
    carrito.agregar(producto);

    expect(carrito.cantidadTotal, 2);
    expect(carrito.total, 196);

    carrito.quitarUno(producto);
    expect(carrito.cantidadTotal, 1);
  });
}
