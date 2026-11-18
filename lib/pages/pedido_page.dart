import 'package:flutter/material.dart';

import '../config/supabase_config.dart';
import '../core/validators.dart';
import '../services/carrito_controller.dart';
import '../services/pedido_service.dart';

class PedidoPage extends StatefulWidget {
  const PedidoPage({super.key, required this.carrito});

  final CarritoController carrito;

  @override
  State<PedidoPage> createState() => _PedidoPageState();
}

class _PedidoPageState extends State<PedidoPage> {
  final _formKey = GlobalKey<FormState>();
  final _nombre = TextEditingController();
  final _telefono = TextEditingController();
  final _service = PedidoService();
  bool _enviando = false;

  @override
  void dispose() {
    _nombre.dispose();
    _telefono.dispose();
    super.dispose();
  }

  Future<void> _confirmar() async {
    if (!_formKey.currentState!.validate()) return;
    if (!SupabaseConfig.isConfigured) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Falta configurar Supabase para crear el pedido.'),
        ),
      );
      return;
    }

    setState(() => _enviando = true);
    try {
      final pedidoId = await _service.crear(
        nombre: _nombre.text,
        telefono: _telefono.text,
        items: widget.carrito.items,
      );
      if (!mounted) return;
      widget.carrito.limpiar();
      await showDialog<void>(
        context: context,
        builder: (_) => AlertDialog(
          title: const Text('Pedido registrado'),
          content: Text('Tu pedido N.º $pedidoId fue enviado al restaurante.'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cerrar'),
            ),
          ],
        ),
      );
      if (mounted) Navigator.pop(context);
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No se pudo registrar el pedido. Intenta nuevamente.'),
        ),
      );
    } finally {
      if (mounted) setState(() => _enviando = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Confirmar pedido')),
    body: Form(
      key: _formKey,
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Text(
            'Datos para el pedido',
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _nombre,
            textCapitalization: TextCapitalization.words,
            decoration: const InputDecoration(labelText: 'Nombre'),
            validator: Validators.requiredName,
          ),
          const SizedBox(height: 14),
          TextFormField(
            controller: _telefono,
            keyboardType: TextInputType.phone,
            decoration: const InputDecoration(labelText: 'Teléfono'),
            validator: Validators.bolivianPhone,
          ),
          const SizedBox(height: 24),
          Text('Total: Bs. ${widget.carrito.total.toStringAsFixed(0)}'),
          const SizedBox(height: 8),
          const Text(
            'La confirmación de disponibilidad será realizada por el restaurante.',
          ),
          const SizedBox(height: 24),
          FilledButton.icon(
            onPressed: _enviando ? null : _confirmar,
            icon: _enviando
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.send),
            label: Text(_enviando ? 'Registrando...' : 'Registrar pedido'),
          ),
        ],
      ),
    ),
  );
}
