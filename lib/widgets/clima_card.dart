import 'package:flutter/material.dart';

import '../core/app_colors.dart';
import '../models/clima.dart';
import '../services/clima_service.dart';

class ClimaCard extends StatefulWidget {
  const ClimaCard({super.key});

  @override
  State<ClimaCard> createState() => _ClimaCardState();
}

class _ClimaCardState extends State<ClimaCard> {
  final _service = ClimaService();
  late Future<Clima> _future;

  @override
  void initState() {
    super.initState();
    _future = _service.obtenerClimaActual();
  }

  void _retry() => setState(() => _future = _service.obtenerClimaActual());

  @override
  Widget build(BuildContext context) => Card(
    color: AppColors.brand.withValues(alpha: .08),
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: FutureBuilder<Clima>(
        future: _future,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Row(
              children: [
                SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2),
                ),
                SizedBox(width: 12),
                Text('Consultando el clima de Santa Cruz...'),
              ],
            );
          }
          if (snapshot.hasError) {
            return Row(
              children: [
                const Expanded(
                  child: Text(
                    'No se pudo obtener el clima. Revisa tu conexión.',
                  ),
                ),
                TextButton(onPressed: _retry, child: const Text('Reintentar')),
              ],
            );
          }
          final clima = snapshot.data!;
          return Row(
            children: [
              const Icon(
                Icons.wb_sunny_outlined,
                color: AppColors.brand,
                size: 38,
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Clima actual en Santa Cruz',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      '${clima.temperatura.toStringAsFixed(0)} °C · ${clima.descripcion}',
                    ),
                  ],
                ),
              ),
            ],
          );
        },
      ),
    ),
  );
}
