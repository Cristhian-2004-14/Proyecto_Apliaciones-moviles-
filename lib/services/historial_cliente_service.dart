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
        .select('id,total,estado,created_at,pagos(id,pedido_id,monto_esperado,estado,created_at,qr_path,beneficiario)')
        .eq('usuario_id', usuario.id)
        .order('created_at', ascending: false);
    return (rows as List)
        .cast<Map<String, dynamic>>()
        .map(PedidoHistorial.fromMap)
        .toList();
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
