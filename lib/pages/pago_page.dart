import 'package:flutter/material.dart';

import '../models/pago.dart';
import '../services/pagos_service.dart';
import 'comprobante_pago_page.dart';

class PagoPage extends StatefulWidget {
  const PagoPage({super.key, required this.pedidoId});
  final int pedidoId;

  @override
  State<PagoPage> createState() => _PagoPageState();
}

class _PagoPageState extends State<PagoPage> {
  final _service = PagosService();
  late Future<Pago> _future;
  bool _downloading = false;

  @override
  void initState() {
    super.initState();
    _future = _service.crearParaPedido(widget.pedidoId);
  }

  void _retry() =>
      setState(() => _future = _service.crearParaPedido(widget.pedidoId));

  Future<void> _descargarQr(Pago pago) async {
    if (pago.qrPath == null) return;
    setState(() => _downloading = true);
    try {
      final saved = await _service.descargarQr(pago.qrPath!);
      if (!mounted) return;
      _message(
        saved ? 'QR guardado en la galería.' : 'No se pudo guardar el QR.',
      );
    } catch (_) {
      _message('No se pudo descargar el QR. Intenta nuevamente.');
    } finally {
      if (mounted) setState(() => _downloading = false);
    }
  }

  void _message(String text) =>
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(text)));

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Pago por QR')),
    body: FutureBuilder<Pago>(
      future: _future,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError) {
          return Center(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.qr_code_2_outlined, size: 58),
                  const SizedBox(height: 12),
                  const Text(
                    'El pedido fue registrado, pero el QR de pago aún no está disponible.',
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 12),
                  FilledButton(
                    onPressed: _retry,
                    child: const Text('Reintentar'),
                  ),
                ],
              ),
            ),
          );
        }
        final pago = snapshot.data!;
        final qrUrl = pago.qrPath == null ? null : _service.urlQr(pago.qrPath!);
        return ListView(
          padding: const EdgeInsets.all(20),
          children: [
            Text(
              'Pedido N.º ${pago.pedidoId}',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            Text(
              'Total exacto: Bs. ${pago.montoEsperado.toStringAsFixed(2)}',
              style: Theme.of(
                context,
              ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            if (qrUrl != null)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      Image.network(
                        qrUrl,
                        height: 250,
                        fit: BoxFit.contain,
                        errorBuilder: (_, _, _) => const SizedBox(
                          height: 180,
                          child: Center(
                            child: Text('No se pudo cargar el QR.'),
                          ),
                        ),
                      ),
                      const SizedBox(height: 12),
                      OutlinedButton.icon(
                        onPressed: _downloading
                            ? null
                            : () => _descargarQr(pago),
                        icon: const Icon(Icons.download_outlined),
                        label: Text(
                          _downloading ? 'Guardando...' : 'Descargar QR',
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            const SizedBox(height: 16),
            const Text(
              '1. Escanea el QR desde tu aplicación bancaria.\n'
              '2. Introduce exactamente el importe mostrado.\n'
              '3. Realiza la transferencia y guarda el comprobante.\n'
              '4. Adjunta el comprobante para su revisión.',
            ),
            if (pago.beneficiario != null) ...[
              const SizedBox(height: 12),
              Text('Beneficiario: ${pago.beneficiario}'),
            ],
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: () async {
                await Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ComprobantePagoPage(pago: pago),
                  ),
                );
                if (mounted) _retry();
              },
              icon: const Icon(Icons.upload_file_outlined),
              label: const Text('Adjuntar comprobante'),
            ),
            const SizedBox(height: 12),
            const Text(
              'Subir un comprobante no confirma el pago. El dueño debe constatar el abono bancario.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 12),
            ),
          ],
        );
      },
    ),
  );
}
