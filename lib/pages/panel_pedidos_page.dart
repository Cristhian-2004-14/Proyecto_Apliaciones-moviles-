import 'package:flutter/material.dart';

import '../core/app_colors.dart';
import '../models/pedido_resumen.dart';
import '../services/panel_pedidos_service.dart';

class PanelPedidosPage extends StatefulWidget {
  const PanelPedidosPage({super.key});

  @override
  State<PanelPedidosPage> createState() => _PanelPedidosPageState();
}

class _PanelPedidosPageState extends State<PanelPedidosPage> {
  final _service = PanelPedidosService();
  late Future<List<PedidoResumen>> _future;

  @override
  void initState() {
    super.initState();
    _future = _service.obtenerPedidos();
  }

  void _retry() => setState(() => _future = _service.obtenerPedidos());

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Panel del dueño')),
    body: FutureBuilder<List<PedidoResumen>>(
      future: _future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError) {
          return Center(
            child: FilledButton(
              onPressed: _retry,
              child: const Text('Reintentar cargar pedidos'),
            ),
          );
        }
        final pedidos = snapshot.data ?? [];
        if (pedidos.isEmpty) {
          return const Center(child: Text('Aún no hay pedidos registrados.'));
        }
        return ListView.separated(
          padding: const EdgeInsets.all(16),
          itemCount: pedidos.length,
          separatorBuilder: (_, _) => const SizedBox(height: 8),
          itemBuilder: (context, index) {
            final pedido = pedidos[index];
            return Card(
              child: ListTile(
                leading: const CircleAvatar(
                  backgroundColor: AppColors.brand,
                  foregroundColor: Colors.white,
                  child: Icon(Icons.receipt_long),
                ),
                title: Text('Pedido N.º ${pedido.id} · ${pedido.nombre}'),
                subtitle: Text('${pedido.telefono}\nEstado: ${pedido.estado}'),
                isThreeLine: true,
                trailing: Text(
                  'Bs. ${pedido.total.toStringAsFixed(0)}',
                  style: const TextStyle(
                    color: AppColors.brand,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            );
          },
        );
      },
    ),
  );
}
