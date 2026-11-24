import 'package:supabase_flutter/supabase_flutter.dart';

import '../models/reserva_resumen.dart';

class ReservaService {
  Future<void> crear({
    required String nombre,
    required String telefono,
    required DateTime fecha,
    required String hora,
    required int personas,
  }) {
    final usuario = Supabase.instance.client.auth.currentUser;
    if (usuario == null) throw StateError('Debes iniciar sesión.');
    return Supabase.instance.client.from('reservas').insert({
      'usuario_id': usuario.id,
      'nombre': nombre.trim(),
      'telefono': telefono.trim(),
      'fecha': fecha.toIso8601String().substring(0, 10),
      'hora': hora,
      'personas': personas,
    });
  }

  Future<List<ReservaResumen>> obtenerTodas() async {
    final rows = await Supabase.instance.client
        .from('reservas')
        .select()
        .order('fecha')
        .order('hora');
    return (rows as List)
        .cast<Map<String, dynamic>>()
        .map(ReservaResumen.fromMap)
        .toList();
  }

  Future<void> actualizarEstado({
    required int reservaId,
    required EstadoReserva estado,
  }) => Supabase.instance.client
      .from('reservas')
      .update({'estado': estado.dbValue})
      .eq('id', reservaId);
}
