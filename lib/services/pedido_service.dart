import 'package:supabase_flutter/supabase_flutter.dart';

import '../models/carrito_item.dart';

class PedidoService {
  Future<int> crear({
    required String nombre,
    required String telefono,
    required List<CarritoItem> items,
  }) async {
    final response = await Supabase.instance.client.rpc(
      'crear_pedido',
      params: {
        'p_nombre': nombre.trim(),
        'p_telefono': telefono.trim(),
        'p_items': items
            .map(
              (item) => {
                'negocio_id': item.producto.id,
                'cantidad': item.cantidad,
              },
            )
            .toList(),
      },
    );
    return (response as num).toInt();
  }
}
