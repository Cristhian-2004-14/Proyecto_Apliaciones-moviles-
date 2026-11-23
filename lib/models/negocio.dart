import 'package:flutter/material.dart';

class Negocio {
  const Negocio({
    required this.id,
    required this.nombre,
    required this.rubro,
    required this.descripcion,
    required this.telefono,
    required this.precio,
    required this.icono,
    this.imagenPath,
  });

  final int id;
  final String nombre;
  final String rubro;
  final String descripcion;
  final String telefono;
  final double precio;
  final IconData icono;
  final String? imagenPath;

  factory Negocio.fromMap(Map<String, dynamic> map) => Negocio(
    id: map['id'] as int,
    nombre: map['nombre'] as String,
    rubro: map['rubro'] as String,
    descripcion: map['descripcion'] as String,
    telefono: map['telefono'] as String,
    precio: (map['precio'] as num?)?.toDouble() ?? 0,
    icono: Icons.outdoor_grill,
    imagenPath: map['imagen_path'] as String?,
  );
}
