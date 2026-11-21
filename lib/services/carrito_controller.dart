import 'dart:collection';

import 'package:flutter/foundation.dart';

import '../models/carrito_item.dart';
import '../models/negocio.dart';

class CarritoController extends ChangeNotifier {
  final List<CarritoItem> _items = [];

  UnmodifiableListView<CarritoItem> get items => UnmodifiableListView(_items);
  int get cantidadTotal =>
      _items.fold(0, (total, item) => total + item.cantidad);
  double get total => _items.fold(0, (total, item) => total + item.subtotal);
  bool get estaVacio => _items.isEmpty;

  void agregar(Negocio producto) {
    final index = _items.indexWhere((item) => item.producto.id == producto.id);
    if (index == -1) {
      _items.add(CarritoItem(producto: producto, cantidad: 1));
    } else {
      final item = _items[index];
      _items[index] = item.copyWith(cantidad: item.cantidad + 1);
    }
    notifyListeners();
  }

  void quitarUno(Negocio producto) {
    final index = _items.indexWhere((item) => item.producto.id == producto.id);
    if (index == -1) return;
    final item = _items[index];
    if (item.cantidad == 1) {
      _items.removeAt(index);
    } else {
      _items[index] = item.copyWith(cantidad: item.cantidad - 1);
    }
    notifyListeners();
  }

  void limpiar() {
    _items.clear();
    notifyListeners();
  }
}
