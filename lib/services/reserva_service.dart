import 'package:supabase_flutter/supabase_flutter.dart';

class ReservaService {
  Future<void> crear({
    required String nombre,
    required String telefono,
    required DateTime fecha,
    required String hora,
    required int personas,
  }) => Supabase.instance.client.from('reservas').insert({
    'nombre': nombre.trim(),
    'telefono': telefono.trim(),
    'fecha': fecha.toIso8601String().substring(0, 10),
    'hora': hora,
    'personas': personas,
  });
}
