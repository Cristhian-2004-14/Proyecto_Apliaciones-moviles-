import 'package:flutter/material.dart';

import '../core/app_colors.dart';
import '../models/reserva_resumen.dart';
import '../services/reserva_service.dart';

class GestionReservasPage extends StatefulWidget {
  const GestionReservasPage({super.key});

  @override
  State<GestionReservasPage> createState() => _GestionReservasPageState();
}

class _GestionReservasPageState extends State<GestionReservasPage> {
  final _service = ReservaService();
  late Future<List<ReservaResumen>> _future;
  int? _actualizandoId;

  @override
  void initState() {
    super.initState();
    _future = _service.obtenerTodas();
  }

  Future<void> _recargar() async {
    setState(() => _future = _service.obtenerTodas());
    await _future;
  }

  Future<void> _cambiarEstado(
    ReservaResumen reserva,
    EstadoReserva estado,
  ) async {
    final accion = estado == EstadoReserva.aceptada ? 'aceptar' : 'denegar';
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('${accion[0].toUpperCase()}${accion.substring(1)} reserva'),
        content: Text(
          '¿Deseas $accion la reserva de ${reserva.nombre} para el ${MaterialLocalizations.of(context).formatMediumDate(reserva.fecha)} a las ${_horaCorta(reserva.hora)}?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: Text(accion[0].toUpperCase() + accion.substring(1)),
          ),
        ],
      ),
    );
    if (confirmar != true) return;

    setState(() => _actualizandoId = reserva.id);
    try {
      await _service.actualizarEstado(reservaId: reserva.id, estado: estado);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Reserva ${estado.label.toLowerCase()} correctamente.')),
      );
      await _recargar();
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('No se pudo actualizar la reserva. Reintenta.')),
      );
    } finally {
      if (mounted) setState(() => _actualizandoId = null);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: const Text('Gestionar reservas'),
      actions: [
        IconButton(
          tooltip: 'Actualizar reservas',
          onPressed: _actualizandoId == null ? _recargar : null,
          icon: const Icon(Icons.refresh),
        ),
      ],
    ),
    body: FutureBuilder<List<ReservaResumen>>(
      future: _future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError) {
          return Center(
            child: FilledButton.icon(
              onPressed: _recargar,
              icon: const Icon(Icons.refresh),
              label: const Text('Reintentar cargar reservas'),
            ),
          );
        }
        final reservas = snapshot.data ?? [];
        if (reservas.isEmpty) {
          return const Center(child: Text('Aún no hay reservas registradas.'));
        }
        return RefreshIndicator(
          onRefresh: _recargar,
          child: ListView.separated(
            padding: const EdgeInsets.all(16),
            itemCount: reservas.length,
            separatorBuilder: (_, _) => const SizedBox(height: 12),
            itemBuilder: (context, index) {
              final reserva = reservas[index];
              final actualizando = _actualizandoId == reserva.id;
              return Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        reserva.nombre,
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                      const SizedBox(height: 6),
                      Text('${reserva.telefono} · ${reserva.personas} personas'),
                      Text(
                        '${MaterialLocalizations.of(context).formatMediumDate(reserva.fecha)} · ${_horaCorta(reserva.hora)}',
                      ),
                      const SizedBox(height: 12),
                      _EstadoReservaChip(estado: reserva.estado),
                      if (reserva.estado == EstadoReserva.solicitada) ...[
                        const SizedBox(height: 14),
                        Row(
                          children: [
                            Expanded(
                              child: FilledButton.icon(
                                onPressed: actualizando
                                    ? null
                                    : () => _cambiarEstado(
                                        reserva,
                                        EstadoReserva.aceptada,
                                      ),
                                style: FilledButton.styleFrom(
                                  minimumSize: const Size.fromHeight(48),
                                  backgroundColor: Colors.green.shade800,
                                ),
                                icon: const Icon(Icons.check),
                                label: const Text('Aceptar'),
                              ),
                            ),
                            const SizedBox(width: 10),
                            Expanded(
                              child: OutlinedButton.icon(
                                onPressed: actualizando
                                    ? null
                                    : () => _cambiarEstado(
                                        reserva,
                                        EstadoReserva.denegada,
                                      ),
                                style: OutlinedButton.styleFrom(
                                  minimumSize: const Size.fromHeight(48),
                                  foregroundColor: Colors.red.shade800,
                                ),
                                icon: const Icon(Icons.close),
                                label: const Text('Denegar'),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ],
                  ),
                ),
              );
            },
          ),
        );
      },
    ),
  );
}

class _EstadoReservaChip extends StatelessWidget {
  const _EstadoReservaChip({required this.estado});
  final EstadoReserva estado;

  @override
  Widget build(BuildContext context) {
    final color = switch (estado) {
      EstadoReserva.aceptada => Colors.green.shade800,
      EstadoReserva.denegada => Colors.red.shade800,
      EstadoReserva.solicitada => AppColors.brand,
    };
    final icon = switch (estado) {
      EstadoReserva.aceptada => Icons.check_circle_outline,
      EstadoReserva.denegada => Icons.cancel_outlined,
      EstadoReserva.solicitada => Icons.hourglass_top_outlined,
    };
    return Semantics(
      label: 'Estado de reserva: ${estado.label}',
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: color, size: 18),
          const SizedBox(width: 6),
          Text(
            'Estado: ${estado.label}',
            style: TextStyle(color: color, fontWeight: FontWeight.w700),
          ),
        ],
      ),
    );
  }
}

String _horaCorta(String hora) => hora.length >= 5 ? hora.substring(0, 5) : hora;
