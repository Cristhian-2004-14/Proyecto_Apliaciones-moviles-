class NegocioConfiguracion {
  const NegocioConfiguracion({
    required this.id,
    required this.nombre,
    this.fotoPath,
  });

  final String id;
  final String nombre;
  final String? fotoPath;

  factory NegocioConfiguracion.fromMap(Map<String, dynamic> map) =>
      NegocioConfiguracion(
        id: map['id'] as String,
        nombre: map['nombre'] as String,
        fotoPath: map['foto_path'] as String?,
      );
}
