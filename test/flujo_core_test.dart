import 'package:conectacruz/models/negocio.dart';
import 'package:conectacruz/models/reserva_resumen.dart';
import 'package:conectacruz/services/carrito_controller.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  const producto = Negocio(
    id: 20,
    nombre: 'Lomo fino',
    rubro: 'Cortes',
    descripcion: 'Producto de prueba',
    telefono: '70000000',
    precio: 84,
    icono: Icons.outdoor_grill,
  );

  test('el carrito elimina el producto al quitar la última unidad', () {
    final carrito = CarritoController();
    carrito.agregar(producto);

    carrito.quitarUno(producto);

    expect(carrito.estaVacio, isTrue);
    expect(carrito.cantidadTotal, 0);
    expect(carrito.total, 0);
  });

  test('un estado de reserva desconocido se mantiene en espera', () {
    final reserva = ReservaResumen.fromMap({
      'id': 10,
      'nombre': 'Cliente de prueba',
      'telefono': '71234567',
      'fecha': '2026-12-01',
      'hora': '19:30:00',
      'personas': 2,
      'estado': 'valor_no_valido',
    });

    expect(reserva.estado, EstadoReserva.solicitada);
    expect(reserva.estado.label, 'EN ESPERA');
  });
}
