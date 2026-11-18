import 'package:supabase_flutter/supabase_flutter.dart';

import '../models/pedido_resumen.dart';

class PanelPedidosService {
  Future<List<PedidoResumen>> obtenerPedidos() async {
    final rows = await Supabase.instance.client
        .from('pedidos')
        .select()
        .order('created_at', ascending: false);
    return (rows as List)
        .cast<Map<String, dynamic>>()
        .map(PedidoResumen.fromMap)
        .toList();
  }
}
