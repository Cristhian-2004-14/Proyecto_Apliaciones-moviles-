import 'package:supabase_flutter/supabase_flutter.dart';

class ConsultaService {
  Future<void> crear({
    required String nombre,
    required String telefono,
    required String mensaje,
  }) => Supabase.instance.client.from('consultas').insert({
    'nombre': nombre.trim(),
    'telefono': telefono.trim(),
    'mensaje': mensaje.trim(),
  });
}
