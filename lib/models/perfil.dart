class Perfil {
  const Perfil({required this.id, required this.nombre, required this.rol});

  final String id;
  final String nombre;
  final String rol;

  bool get esDueno => rol == 'dueno';

  factory Perfil.fromMap(Map<String, dynamic> map) {
    final nombre = (map['nombre'] as String? ?? '').trim();
    return Perfil(
      id: map['id'] as String,
      nombre: nombre.isEmpty ? 'Cliente' : nombre,
      rol: map['rol'] as String? ?? 'cliente',
    );
  }
}
