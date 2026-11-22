import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../services/pagos_service.dart';

class ConfiguracionQrPage extends StatefulWidget {
  const ConfiguracionQrPage({super.key});

  @override
  State<ConfiguracionQrPage> createState() => _ConfiguracionQrPageState();
}

class _ConfiguracionQrPageState extends State<ConfiguracionQrPage> {
  final _service = PagosService();
  final _picker = ImagePicker();
  final _form = GlobalKey<FormState>();
  final _beneficiario = TextEditingController();
  final _cuenta = TextEditingController();
  XFile? _qr;
  bool _saving = false;

  @override
  void dispose() {
    _beneficiario.dispose();
    _cuenta.dispose();
    super.dispose();
  }

  Future<void> _pickQr() async {
    final image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null && mounted) setState(() => _qr = image);
  }

  Future<void> _save() async {
    if (!_form.currentState!.validate() || _qr == null) {
      if (_qr == null) _message('Selecciona la imagen del QR bancario.');
      return;
    }
    setState(() => _saving = true);
    try {
      await _service.guardarConfiguracionQr(
        image: _qr!,
        beneficiario: _beneficiario.text,
        cuentaDestino: _cuenta.text,
      );
      if (!mounted) return;
      _message('QR de pago configurado correctamente.');
      Navigator.pop(context);
    } catch (error) {
      _message('No se pudo guardar el QR: $error');
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  void _message(String text) =>
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(text)));

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Configurar QR de pagos')),
    body: Form(
      key: _form,
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Text(
            'Carga únicamente un QR real y autorizado. Los datos se guardan en Supabase, no en el código.',
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _beneficiario,
            decoration: const InputDecoration(
              labelText: 'Beneficiario esperado',
            ),
            validator: (value) =>
                (value ?? '').trim().isEmpty ? 'Campo obligatorio.' : null,
          ),
          const SizedBox(height: 12),
          TextFormField(
            controller: _cuenta,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Cuenta receptora para validación',
            ),
            validator: (value) => (value ?? '').trim().length < 5
                ? 'Ingresa una cuenta válida.'
                : null,
          ),
          const SizedBox(height: 18),
          OutlinedButton.icon(
            onPressed: _saving ? null : _pickQr,
            icon: const Icon(Icons.qr_code_2_outlined),
            label: Text(_qr == null ? 'Seleccionar imagen QR' : _qr!.name),
          ),
          const SizedBox(height: 20),
          FilledButton.icon(
            onPressed: _saving ? null : _save,
            icon: _saving
                ? const SizedBox(
                    width: 18,
                    height: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.save_outlined),
            label: const Text('Guardar configuración'),
          ),
        ],
      ),
    ),
  );
}
