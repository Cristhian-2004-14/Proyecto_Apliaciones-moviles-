import 'package:flutter/material.dart';

import '../core/app_colors.dart';
import '../models/pago.dart';
import '../models/pedido_historial.dart';
import '../models/reserva_resumen.dart';
import '../services/historial_cliente_service.dart';

class MisPedidosReservasPage extends StatefulWidget {
  const MisPedidosReservasPage({super.key});

  @override
  State<MisPedidosReservasPage> createState() => _MisPedidosReservasPageState();
}

class _MisPedidosReservasPageState extends State<MisPedidosReservasPage> {
  final _service = HistorialClienteService();
  late Future<List<PedidoHistorial>> _pedidosFuture;
  late Future<List<ReservaResumen>> _reservasFuture;

  @override
  void initState() {
    super.initState();
    _pedidosFuture = _service.obtenerPedidos();
    _reservasFuture = _service.obtenerReservas();
  }

  Future<void> _recargarPedidos() async {
    final future = _service.obtenerPedidos();
    setState(() => _pedidosFuture = future);
    await future;
  }

  Future<void> _recargarReservas() async {
    final future = _service.obtenerReservas();
    setState(() => _reservasFuture = future);
    await future;
  }

  @override
  Widget build(BuildContext context) => DefaultTabController(
    length: 2,
    child: Scaffold(
      appBar: AppBar(
        title: const Text('Mis pedidos y reservas'),
        bottom: const TabBar(
          tabs: [
            Tab(icon: Icon(Icons.receipt_long_outlined), text: 'Pedidos'),
            Tab(icon: Icon(Icons.event_seat_outlined), text: 'Reservas'),
          ],
        ),
      ),
      body: TabBarView(
        children: [
          FutureBuilder<List<PedidoHistorial>>(
            future: _pedidosFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState != ConnectionState.done) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError) {
                return _EstadoVacio(
                  icon: Icons.cloud_off_outlined,
                  mensaje: 'No se pudieron cargar tus pedidos.',
                  boton: 'Reintentar',
                  onPressed: _recargarPedidos,
                );
              }
              return _ListaPedidos(
                pedidos: snapshot.data ?? [],
                onRefresh: _recargarPedidos,
              );
            },
          ),
          FutureBuilder<List<ReservaResumen>>(
            future: _reservasFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState != ConnectionState.done) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError) {
                return _EstadoVacio(
                  icon: Icons.cloud_off_outlined,
                  mensaje: 'No se pudieron cargar tus reservas. Ejecuta el SQL 10 en Supabase y reintenta.',
                  boton: 'Reintentar',
                  onPressed: _recargarReservas,
                );
              }
              return _ListaReservas(
                reservas: snapshot.data ?? [],
                onRefresh: _recargarReservas,
              );
            },
          ),
        ],
      ),
    ),
  );
}

class _ListaPedidos extends StatelessWidget {
  const _ListaPedidos({required this.pedidos, required this.onRefresh});
  final List<PedidoHistorial> pedidos;
  final Future<void> Function() onRefresh;

  @override
  Widget build(BuildContext context) {
    if (pedidos.isEmpty) {
      return _EstadoVacio(
        icon: Icons.receipt_long_outlined,
        mensaje: 'Todavía no tienes pedidos registrados.',
        boton: 'Actualizar',
        onPressed: onRefresh,
      );
    }
    return RefreshIndicator(
      onRefresh: onRefresh,
      child: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: pedidos.length,
        separatorBuilder: (_, _) => const SizedBox(height: 12),
        itemBuilder: (context, index) {
          final pedido = pedidos[index];
          final pago = pedido.pago;
          final estadoCliente = _estadoPedidoCliente(pago);
          return Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.receipt_long_outlined, color: AppColors.brand),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          'Pedido N.º ${pedido.id}',
                          style: Theme.of(context).textTheme.titleMedium,
                        ),
                      ),
                      Text(
                        'Bs. ${pedido.total.toStringAsFixed(2)}',
                        style: const TextStyle(
                          color: AppColors.brand,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text('Estado del pedido: ${estadoCliente.label}'),
                  Text(
                    'Fecha: ${MaterialLocalizations.of(context).formatMediumDate(pedido.fecha)}',
                  ),
                  const SizedBox(height: 12),
                  _EstadoEtiqueta(
                    icon: estadoCliente.icon,
                    texto: 'PEDIDO: ${estadoCliente.label}',
                    color: estadoCliente.color,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    pago == null
                        ? 'Pago: aún no iniciado'
                        : 'Revisión de pago: ${pago.estado.label}',
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

class _ListaReservas extends StatelessWidget {
  const _ListaReservas({required this.reservas, required this.onRefresh});
  final List<ReservaResumen> reservas;
  final Future<void> Function() onRefresh;

  @override
  Widget build(BuildContext context) {
    if (reservas.isEmpty) {
      return _EstadoVacio(
        icon: Icons.event_seat_outlined,
        mensaje: 'Todavía no tienes reservas registradas.',
        boton: 'Actualizar',
        onPressed: onRefresh,
      );
    }
    return RefreshIndicator(
      onRefresh: onRefresh,
      child: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: reservas.length,
        separatorBuilder: (_, _) => const SizedBox(height: 12),
        itemBuilder: (context, index) {
          final reserva = reservas[index];
          final color = switch (reserva.estado) {
            EstadoReserva.aceptada => Colors.green.shade800,
            EstadoReserva.denegada => Colors.red.shade800,
            EstadoReserva.solicitada => AppColors.brand,
          };
          return Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Reserva N.º ${reserva.id}',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '${MaterialLocalizations.of(context).formatMediumDate(reserva.fecha)} · ${_horaCorta(reserva.hora)}',
                  ),
                  Text('${reserva.personas} ${reserva.personas == 1 ? 'persona' : 'personas'}'),
                  const SizedBox(height: 12),
                  _EstadoEtiqueta(
                    icon: reserva.estado == EstadoReserva.aceptada
                        ? Icons.check_circle_outline
                        : reserva.estado == EstadoReserva.denegada
                        ? Icons.cancel_outlined
                        : Icons.hourglass_top_outlined,
                    texto: 'RESERVA: ${reserva.estado.label}',
                    color: color,
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

class _EstadoEtiqueta extends StatelessWidget {
  const _EstadoEtiqueta({
    required this.icon,
    required this.texto,
    required this.color,
  });
  final IconData icon;
  final String texto;
  final Color color;

  @override
  Widget build(BuildContext context) => Semantics(
    label: texto,
    child: Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: color.withValues(alpha: .10),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 18, color: color),
          const SizedBox(width: 6),
          Text(texto, style: TextStyle(color: color, fontWeight: FontWeight.w700)),
        ],
      ),
    ),
  );
}

class _EstadoVacio extends StatelessWidget {
  const _EstadoVacio({
    required this.icon,
    required this.mensaje,
    required this.boton,
    required this.onPressed,
  });
  final IconData icon;
  final String mensaje;
  final String boton;
  final Future<void> Function() onPressed;

  @override
  Widget build(BuildContext context) => Center(
    child: Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 52, color: AppColors.brand),
          const SizedBox(height: 16),
          Text(mensaje, textAlign: TextAlign.center),
          const SizedBox(height: 16),
          OutlinedButton.icon(
            onPressed: onPressed,
            icon: const Icon(Icons.refresh),
            label: Text(boton),
          ),
        ],
      ),
    ),
  );
}

class _EstadoPedidoCliente {
  const _EstadoPedidoCliente({
    required this.label,
    required this.color,
    required this.icon,
  });

  final String label;
  final Color color;
  final IconData icon;
}

_EstadoPedidoCliente _estadoPedidoCliente(Pago? pago) {
  if (pago?.estado == EstadoPago.pagado) {
    return _EstadoPedidoCliente(
      label: 'CONFIRMADO',
      color: Colors.green.shade800,
      icon: Icons.check_circle_outline,
    );
  }
  if (pago?.estado == EstadoPago.rechazado) {
    return _EstadoPedidoCliente(
      label: 'RECHAZADO',
      color: Colors.red.shade800,
      icon: Icons.cancel_outlined,
    );
  }
  return const _EstadoPedidoCliente(
    label: 'EN ESPERA',
    color: AppColors.brand,
    icon: Icons.hourglass_top_outlined,
  );
}

String _horaCorta(String hora) => hora.length >= 5 ? hora.substring(0, 5) : hora;
