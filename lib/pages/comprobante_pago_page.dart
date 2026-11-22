import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../models/pago.dart';
import '../services/pagos_service.dart';

class ComprobantePagoPage extends StatefulWidget {
  const ComprobantePagoPage({super.key, required this.pago});
  final Pago pago;

  @override
  State<ComprobantePagoPage> createState() => _ComprobantePagoPageState();
}

class _ComprobantePagoPageState extends State<ComprobantePagoPage> {
  final _picker = ImagePicker();
  final _service = PagosService();
  XFile? _image;
  bool _processing = false;

  Future<void> _select() async {
    final image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null && mounted) setState(() => _image = image);
  }

  Future<void> _upload() async {
    final image = _image;
    if (image == null) return;
    setState(() => _processing = true);
    try {
      final pago = await _service.cargarComprobante(
        pago: widget.pago,
        image: image,
      );
      if (!mounted) return;
      await showDialog<void>(
        context: context,
        builder: (_) => AlertDialog(
          title: const Text('Comprobante recibido'),
          content: Text(
            pago.estado == EstadoPago.comprobanteValidado
                ? 'Los datos coinciden. Aún falta la constatación bancaria del dueño.'
                : 'El comprobante fue enviado a revisión manual.',
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Aceptar'),
            ),
          ],
        ),
      );
      if (mounted) Navigator.pop(context, true);
    } catch (error) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('No se pudo procesar el comprobante: $error')),
        );
      }
    } finally {
      if (mounted) setState(() => _processing = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Adjuntar comprobante')),
    body: ListView(
      padding: const EdgeInsets.all(20),
      children: [
        const Text('Aceptamos imágenes JPG o PNG de hasta 5 MB.'),
        const SizedBox(height: 20),
        OutlinedButton.icon(
          onPressed: _processing ? null : _select,
          icon: const Icon(Icons.photo_library_outlined),
          label: const Text('Seleccionar comprobante'),
        ),
        if (_image != null) ...[
          const SizedBox(height: 16),
          Text('Archivo seleccionado: ${_image!.name}'),
        ],
        const SizedBox(height: 20),
        FilledButton.icon(
          onPressed: _processing || _image == null ? null : _upload,
          icon: _processing
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Icon(Icons.document_scanner_outlined),
          label: Text(
            _processing ? 'Leyendo y enviando...' : 'Validar y enviar',
          ),
        ),
        const SizedBox(height: 12),
        const Text(
          'La lectura OCR es una ayuda documental; no acredita por sí sola que el dinero ingresó.',
          textAlign: TextAlign.center,
          style: TextStyle(fontSize: 12),
        ),
      ],
    ),
  );
}
