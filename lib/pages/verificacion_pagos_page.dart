import 'package:flutter/material.dart';

import '../models/comprobante_ocr.dart';
import '../models/pago.dart';
import '../services/pagos_service.dart';

class VerificacionPagosPage extends StatefulWidget {
  const VerificacionPagosPage({super.key});

  @override
  State<VerificacionPagosPage> createState() => _VerificacionPagosPageState();
}

class _VerificacionPagosPageState extends State<VerificacionPagosPage> {
  final _service = PagosService();
  late Future<List<PagoAdmin>> _future;
  String _filter = '';

  @override
  void initState() {
    super.initState();
    _future = _service.obtenerPagosAdmin();
  }

  void _reload() => setState(() => _future = _service.obtenerPagosAdmin());

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Verificación de pagos')),
    body: FutureBuilder<List<PagoAdmin>>(
      future: _future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError) {
          return Center(
            child: FilledButton(
              onPressed: _reload,
              child: const Text('Reintentar'),
            ),
          );
        }
        final payments = (snapshot.data ?? []).where((payment) {
          final term = _filter.toLowerCase();
          return term.isEmpty ||
              '${payment.pedidoId}'.contains(term) ||
              payment.estado.label.toLowerCase().contains(term) ||
              (payment.cliente ?? '').toLowerCase().contains(term);
        }).toList();
        return Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(16),
              child: TextField(
                decoration: const InputDecoration(
                  prefixIcon: Icon(Icons.search),
                  labelText: 'Buscar pedido, cliente o estado',
                ),
                onChanged: (value) => setState(() => _filter = value),
              ),
            ),
            Expanded(
              child: payments.isEmpty
                  ? const Center(child: Text('No hay pagos para revisar.'))
                  : ListView.builder(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      itemCount: payments.length,
                      itemBuilder: (_, index) => Card(
                        child: ListTile(
                          title: Text(
                            'Pedido N.º ${payments[index].pedidoId} · ${payments[index].cliente ?? 'Cliente'}',
                          ),
                          subtitle: Text(
                            '${payments[index].estado.label}\n${payments[index].createdAt}',
                          ),
                          isThreeLine: true,
                          trailing: Text(
                            'Bs. ${payments[index].montoEsperado.toStringAsFixed(2)}',
                          ),
                          onTap: () async {
                            await Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) =>
                                    _DetallePagoPage(pago: payments[index]),
                              ),
                            );
                            _reload();
                          },
                        ),
                      ),
                    ),
            ),
          ],
        );
      },
    ),
  );
}

class _DetallePagoPage extends StatefulWidget {
  const _DetallePagoPage({required this.pago});
  final PagoAdmin pago;

  @override
  State<_DetallePagoPage> createState() => _DetallePagoPageState();
}

class _DetallePagoPageState extends State<_DetallePagoPage> {
  final _service = PagosService();
  late Future<List<ComprobantePago>> _future;

  @override
  void initState() {
    super.initState();
    _future = _service.obtenerComprobantes(widget.pago.id);
  }

  Future<void> _resolve(bool approve) async {
    final notes = TextEditingController();
    final reference = TextEditingController();
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(
          approve ? 'Confirmar abono bancario' : 'Rechazar comprobante',
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              approve
                  ? 'Confirma solo después de revisar el abono real en la banca autorizada.'
                  : 'Indica el motivo del rechazo.',
            ),
            TextField(
              controller: notes,
              decoration: const InputDecoration(labelText: 'Observaciones'),
            ),
            if (approve)
              TextField(
                controller: reference,
                decoration: const InputDecoration(
                  labelText: 'Referencia de constatación',
                ),
              ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Confirmar'),
          ),
        ],
      ),
    );
    if (confirmed != true) return;
    try {
      await _service.resolverComoDueno(
        pagoId: widget.pago.id,
        aprobar: approve,
        observaciones: notes.text,
        referenciaConstatacion: reference.text,
      );
      if (mounted) {
        Navigator.pop(context);
      }
    } catch (error) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('$error')));
      }
    } finally {
      notes.dispose();
      reference.dispose();
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: Text('Pago del pedido ${widget.pago.pedidoId}')),
    body: FutureBuilder<List<ComprobantePago>>(
      future: _future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(child: CircularProgressIndicator());
        }
        final proofs = snapshot.data ?? [];
        return ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Text('Estado: ${widget.pago.estado.label}'),
            Text('Monto: Bs. ${widget.pago.montoEsperado.toStringAsFixed(2)}'),
            const SizedBox(height: 16),
            const Text(
              'Comprobantes recibidos',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            if (proofs.isEmpty)
              const Padding(
                padding: EdgeInsets.only(top: 12),
                child: Text('Aún no se adjuntó ningún comprobante.'),
              ),
            ...proofs.map(
              (proof) => Card(
                child: ListTile(
                  leading: const Icon(Icons.receipt_long_outlined),
                  title: Text(
                    proof.codigoOperacion ?? 'Sin código de operación',
                  ),
                  subtitle: Text(
                    'Banco: ${proof.banco ?? 'No identificado'}\nMonto: ${proof.monto?.toStringAsFixed(2) ?? 'No identificado'}',
                  ),
                  isThreeLine: true,
                  onTap: () async {
                    final url = await _service.urlComprobanteFirmada(
                      proof.ruta,
                    );
                    if (!context.mounted) return;
                    await showDialog<void>(
                      context: context,
                      builder: (_) => Dialog(child: Image.network(url)),
                    );
                  },
                ),
              ),
            ),
            const SizedBox(height: 20),
            if (widget.pago.estado != EstadoPago.pagado) ...[
              FilledButton.icon(
                onPressed: () => _resolve(true),
                icon: const Icon(Icons.verified_outlined),
                label: const Text('Confirmar abono y marcar PAGADO'),
              ),
              const SizedBox(height: 8),
              OutlinedButton.icon(
                onPressed: () => _resolve(false),
                icon: const Icon(Icons.close),
                label: const Text('Rechazar comprobante'),
              ),
            ],
          ],
        );
      },
    ),
  );
}
