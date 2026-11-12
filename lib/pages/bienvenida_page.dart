import 'package:flutter/material.dart';

import '../core/app_colors.dart';
import 'inicio_page.dart';

class BienvenidaPage extends StatelessWidget {
  const BienvenidaPage({super.key});

  @override
  Widget build(BuildContext context) => Scaffold(
    body: SafeArea(
      child: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.outdoor_grill, color: AppColors.brand, size: 88),
              const SizedBox(height: 20),
              Text(
                'Brasas del Oriente',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                  color: AppColors.coal,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 10),
              const Text(
                'El sabor de la parrilla cruceña, cerca de ti.',
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              FilledButton.icon(
                style: FilledButton.styleFrom(
                  minimumSize: const Size.fromHeight(54),
                  backgroundColor: AppColors.brand,
                ),
                onPressed: () => Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (_) => const InicioPage()),
                ),
                icon: const Icon(Icons.restaurant_menu),
                label: const Text('Entrar a la churrasquería'),
              ),
            ],
          ),
        ),
      ),
    ),
  );
}
