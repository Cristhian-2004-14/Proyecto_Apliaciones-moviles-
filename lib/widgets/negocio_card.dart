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
    child: Padding(
      padding: const EdgeInsets.all(14),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(width: 64, height: 64, child: Center(child: _imagen())),
          const SizedBox(width: 12),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(top: 2),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    negocio.nombre,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    negocio.descripcion,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(width: 8),
          SizedBox(
            width: 52,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  'Bs. ${negocio.precio.toStringAsFixed(0)}',
                  textAlign: TextAlign.end,
                  style: const TextStyle(
                    color: AppColors.brand,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                SizedBox(
                  width: 44,
                  height: 44,
                  child: IconButton(
                    tooltip: 'Agregar al pedido',
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints.tightFor(
                      width: 44,
                      height: 44,
                    ),
                    onPressed: onAdd,
                    icon: const Icon(Icons.add_circle, color: AppColors.brand),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}
