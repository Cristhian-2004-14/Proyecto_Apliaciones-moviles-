import 'negocio.dart';

class CarritoItem {
  const CarritoItem({required this.producto, required this.cantidad});

  final Negocio producto;
  final int cantidad;

  double get subtotal => producto.precio * cantidad;

  CarritoItem copyWith({int? cantidad}) =>
      CarritoItem(producto: producto, cantidad: cantidad ?? this.cantidad);
}
