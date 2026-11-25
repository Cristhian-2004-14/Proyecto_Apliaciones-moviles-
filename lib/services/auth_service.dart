import 'package:supabase_flutter/supabase_flutter.dart';

import '../models/perfil.dart';

class AuthService {
  SupabaseClient get _client => Supabase.instance.client;

  User? get usuarioActual => _client.auth.currentUser;

  Future<void> iniciarSesion({
    required String email,
    required String password,
  }) =>
      _client.auth.signInWithPassword(email: email.trim(), password: password);

  Future<AuthResponse> registrar({
    required String nombre,
    required String email,
    required String password,
  }) => _client.auth.signUp(
    email: email.trim(),
    password: password,
    data: {'nombre': nombre.trim()},
  );

  Future<void> cerrarSesion() => _client.auth.signOut();

  Future<Perfil?> obtenerPerfil() async {
    final user = usuarioActual;
    if (user == null) return null;
    final row = await _client
        .from('perfiles')
        .select()
        .eq('id', user.id)
        .maybeSingle();
    return row == null ? null : Perfil.fromMap(row);
  }
}
