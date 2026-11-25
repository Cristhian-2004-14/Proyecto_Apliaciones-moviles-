import 'package:supabase_flutter/supabase_flutter.dart';

import '../models/pedido_historial.dart';
import '../models/reserva_resumen.dart';

class HistorialClienteService {
  SupabaseClient get _client => Supabase.instance.client;

  Future<List<PedidoHistorial>> obtenerPedidos() async {
    final usuario = _client.auth.currentUser;
    if (usuario == null) throw StateError('Debes iniciar sesión.');
    final rows = await _client
        .from('pedidos')
        .select('id,total,estado,created_at')
        .eq('usuario_id', usuario.id)
        .order('created_at', ascending: false);
    final pedidos = (rows as List).cast<Map<String, dynamic>>();
    if (pedidos.isEmpty) return const [];

    // Un error al consultar pagos no debe ocultar los pedidos del cliente.
    final ids = pedidos.map((pedido) => pedido['id']).toList();
    final pagosPorPedido = <int, Map<String, dynamic>>{};
    try {
      final pagos = await _client
          .from('pagos')
          .select('id,pedido_id,monto_esperado,estado,created_at')
          .inFilter('pedido_id', ids);
      for (final pago in (pagos as List).cast<Map<String, dynamic>>()) {
        final pedidoId = (pago['pedido_id'] as num).toInt();
        pagosPorPedido.putIfAbsent(pedidoId, () => pago);
      }
    } catch (_) {
      // Si el módulo de pagos no está disponible, el pedido queda EN ESPERA.
    }

    return pedidos.map((pedido) {
      final copy = Map<String, dynamic>.from(pedido);
      final pago = pagosPorPedido[pedido['id'] as int];
      if (pago != null) copy['pagos'] = [pago];
      return PedidoHistorial.fromMap(copy);
    }).toList();
  }

  Future<List<ReservaResumen>> obtenerReservas() async {
    final usuario = _client.auth.currentUser;
    if (usuario == null) throw StateError('Debes iniciar sesión.');
    final rows = await _client
        .from('reservas')
        .select()
        .eq('usuario_id', usuario.id)
        .order('fecha', ascending: false)
        .order('hora', ascending: false);
    return (rows as List)
        .cast<Map<String, dynamic>>()
        .map(ReservaResumen.fromMap)
        .toList();
  }
}
