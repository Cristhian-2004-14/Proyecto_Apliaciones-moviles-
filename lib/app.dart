import 'package:flutter/material.dart';

import 'core/app_theme.dart';
import 'pages/bienvenida_page.dart';
import 'services/carrito_controller.dart';

class BrasasDelOrienteApp extends StatefulWidget {
  const BrasasDelOrienteApp({super.key});

  @override
  State<BrasasDelOrienteApp> createState() => _BrasasDelOrienteAppState();
}

class _BrasasDelOrienteAppState extends State<BrasasDelOrienteApp> {
  final _carrito = CarritoController();

  @override
  void dispose() {
    _carrito.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Brasas del Oriente',
    debugShowCheckedModeBanner: false,
    theme: AppTheme.light,
    home: BienvenidaPage(carrito: _carrito),
  );
}
