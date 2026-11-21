import 'package:flutter/material.dart';

import '../core/app_colors.dart';
import '../models/negocio.dart';

class NegocioCard extends StatelessWidget {
  const NegocioCard({super.key, required this.negocio, required this.onAdd});

  final Negocio negocio;
  final VoidCallback onAdd;

  @override
  Widget build(BuildContext context) => Card(
    child: ListTile(
      contentPadding: const EdgeInsets.all(14),
      leading: CircleAvatar(
        backgroundColor: AppColors.brand.withValues(alpha: .12),
        foregroundColor: AppColors.brand,
        radius: 25,
        child: Icon(negocio.icono),
      ),
      title: Text(
        negocio.nombre,
        style: const TextStyle(fontWeight: FontWeight.bold),
      ),
      subtitle: Text(negocio.descripcion),
      trailing: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            'Bs. ${negocio.precio.toStringAsFixed(0)}',
            style: const TextStyle(
              color: AppColors.brand,
              fontWeight: FontWeight.bold,
            ),
          ),
          IconButton(
            tooltip: 'Agregar al pedido',
            onPressed: onAdd,
            icon: const Icon(Icons.add_circle, color: AppColors.brand),
          ),
        ],
      ),
    ),
  );
}
