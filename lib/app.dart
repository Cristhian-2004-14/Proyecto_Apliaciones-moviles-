import 'package:flutter/material.dart';

import 'core/app_theme.dart';
import 'pages/bienvenida_page.dart';

class BrasasDelOrienteApp extends StatelessWidget {
  const BrasasDelOrienteApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Brasas del Oriente',
    debugShowCheckedModeBanner: false,
    theme: AppTheme.light,
    home: const BienvenidaPage(),
  );
}
