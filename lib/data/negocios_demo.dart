import 'package:flutter/material.dart';

import '../models/negocio.dart';

const restaurantPhone = '70000000';

const negociosDemo = <Negocio>[
  Negocio(
    id: 1,
    nombre: 'Parrillada Oriente',
    rubro: 'Parrilladas',
    descripcion: 'Carne, chorizo, pollo y guarniciones para compartir.',
    telefono: restaurantPhone,
    precio: 98,
    icono: Icons.outdoor_grill,
  ),
  Negocio(
    id: 2,
    nombre: 'Bife de chorizo',
    rubro: 'Cortes',
    descripcion: 'Corte jugoso de res a la brasa, 350 g.',
    telefono: restaurantPhone,
    precio: 72,
    icono: Icons.restaurant,
  ),
  Negocio(
    id: 3,
    nombre: 'Lomo fino',
    rubro: 'Cortes',
    descripcion: 'Medallón de res con salsa de la casa.',
    telefono: restaurantPhone,
    precio: 84,
    icono: Icons.local_fire_department,
  ),
  Negocio(
    id: 4,
    nombre: 'Yuca al horno',
    rubro: 'Acompañamientos',
    descripcion: 'Yuca dorada con mantequilla de hierbas.',
    telefono: restaurantPhone,
    precio: 15,
    icono: Icons.bakery_dining,
  ),
  Negocio(
    id: 5,
    nombre: 'Ensalada criolla',
    rubro: 'Acompañamientos',
    descripcion: 'Tomate, cebolla y locoto fresco.',
    telefono: restaurantPhone,
    precio: 18,
    icono: Icons.eco,
  ),
  Negocio(
    id: 6,
    nombre: 'Mocochinchi',
    rubro: 'Bebidas',
    descripcion: 'Bebida tradicional fría.',
    telefono: restaurantPhone,
    precio: 14,
    icono: Icons.local_drink,
  ),
  Negocio(
    id: 7,
    nombre: 'Limonada de hierbabuena',
    rubro: 'Bebidas',
    descripcion: 'Refrescante y natural.',
    telefono: restaurantPhone,
    precio: 16,
    icono: Icons.emoji_food_beverage,
  ),
];
