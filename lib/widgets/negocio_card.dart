import 'package:flutter/material.dart';

import '../core/app_colors.dart';
import '../models/negocio.dart';
import '../services/storage_service.dart';

class NegocioCard extends StatelessWidget {
  const NegocioCard({super.key, required this.negocio, required this.onAdd});

  final Negocio negocio;
  final VoidCallback onAdd;

  Widget _imagen() {
    final url = StorageService().urlPublica(negocio.imagenPath);
    if (url == null) {
      return CircleAvatar(
        backgroundColor: AppColors.brand.withValues(alpha: .12),
        foregroundColor: AppColors.brand,
        radius: 30,
        child: Icon(negocio.icono),
      );
    }
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: Image.network(
        '$url?t=${DateTime.now().millisecondsSinceEpoch}',
        width: 64,
        height: 64,
        fit: BoxFit.cover,
        errorBuilder: (_, _, _) => CircleAvatar(
          backgroundColor: AppColors.brand.withValues(alpha: .12),
          foregroundColor: AppColors.brand,
          radius: 30,
          child: Icon(negocio.icono),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => Card(
    child: ListTile(
      contentPadding: const EdgeInsets.all(14),
      leading: _imagen(),
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
