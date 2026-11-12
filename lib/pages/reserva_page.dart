import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../core/app_colors.dart';
import '../core/validators.dart';
import '../config/supabase_config.dart';
import '../services/reserva_service.dart';

class ReservaPage extends StatefulWidget {
  const ReservaPage({super.key});

  @override
  State<ReservaPage> createState() => _ReservaPageState();
}

class _ReservaPageState extends State<ReservaPage> {
  final _formKey = GlobalKey<FormState>();
  final _name = TextEditingController();
  final _phone = TextEditingController();
  final _people = TextEditingController(text: '2');
  final _service = ReservaService();
  DateTime? _date;
  TimeOfDay? _time;
  bool _sending = false;

  @override
  void dispose() {
    _name.dispose();
    _phone.dispose();
    _people.dispose();
    super.dispose();
  }

  Future<void> _pickDate() async {
    final now = DateTime.now();
    final selected = await showDatePicker(
      context: context,
      initialDate: _date ?? now,
      firstDate: DateTime(now.year, now.month, now.day),
      lastDate: now.add(const Duration(days: 180)),
    );
    if (selected != null) setState(() => _date = selected);
  }

  Future<void> _pickTime() async {
    final selected = await showTimePicker(
      context: context,
      initialTime: _time ?? const TimeOfDay(hour: 20, minute: 0),
    );
    if (selected != null) setState(() => _time = selected);
  }

  bool _isPastDateTime() {
    if (_date == null || _time == null) return false;
    final selected = DateTime(
      _date!.year,
      _date!.month,
      _date!.day,
      _time!.hour,
      _time!.minute,
    );
    return !selected.isAfter(DateTime.now());
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate() || _date == null || _time == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Completa todos los datos de la reserva.'),
        ),
      );
      return;
    }
    if (_isPastDateTime()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('La fecha y hora de la reserva deben ser futuras.'),
        ),
      );
      return;
    }
    if (!SupabaseConfig.isConfigured) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Falta configurar Supabase para enviar la reserva.'),
        ),
      );
      return;
    }
    setState(() => _sending = true);
    try {
      await _service.crear(
        nombre: _name.text,
        telefono: _phone.text,
        fecha: _date!,
        hora:
            '${_time!.hour.toString().padLeft(2, '0')}:${_time!.minute.toString().padLeft(2, '0')}:00',
        personas: int.parse(_people.text),
      );
      if (!mounted) return;
      showDialog<void>(
        context: context,
        builder: (_) => AlertDialog(
          title: const Text('Reserva enviada'),
          content: const Text(
            'La reserva fue registrada correctamente. El restaurante deberá confirmar la disponibilidad.',
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cerrar'),
            ),
          ],
        ),
      );
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No se pudo enviar la reserva. Intenta nuevamente.'),
        ),
      );
    } finally {
      if (mounted) setState(() => _sending = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Reservar mesa')),
    body: Form(
      key: _formKey,
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Text(
            'Solicita tu mesa',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 6),
          const Text(
            'La confirmación final depende de la disponibilidad del restaurante.',
          ),
          const SizedBox(height: 22),
          TextFormField(
            controller: _name,
            decoration: const InputDecoration(
              labelText: 'Nombre del cliente',
              prefixIcon: Icon(Icons.person),
            ),
            validator: Validators.requiredName,
          ),
          const SizedBox(height: 14),
          TextFormField(
            controller: _phone,
            keyboardType: TextInputType.phone,
            inputFormatters: [
              FilteringTextInputFormatter.digitsOnly,
              LengthLimitingTextInputFormatter(8),
            ],
            decoration: const InputDecoration(
              labelText: 'Teléfono boliviano',
              hintText: 'Ej.: 71234567',
              prefixIcon: Icon(Icons.phone),
            ),
            validator: Validators.bolivianPhone,
          ),
          const SizedBox(height: 14),
          OutlinedButton.icon(
            onPressed: _pickDate,
            icon: const Icon(Icons.calendar_today),
            label: Text(
              _date == null
                  ? 'Seleccionar fecha'
                  : MaterialLocalizations.of(context).formatMediumDate(_date!),
            ),
          ),
          const SizedBox(height: 10),
          OutlinedButton.icon(
            onPressed: _pickTime,
            icon: const Icon(Icons.access_time),
            label: Text(
              _time == null ? 'Seleccionar hora' : _time!.format(context),
            ),
          ),
          const SizedBox(height: 14),
          TextFormField(
            controller: _people,
            keyboardType: TextInputType.number,
            inputFormatters: [
              FilteringTextInputFormatter.digitsOnly,
              LengthLimitingTextInputFormatter(2),
            ],
            decoration: const InputDecoration(
              labelText: 'Cantidad de personas',
              prefixIcon: Icon(Icons.groups),
            ),
            validator: Validators.people,
          ),
          const SizedBox(height: 24),
          FilledButton.icon(
            style: FilledButton.styleFrom(
              minimumSize: const Size.fromHeight(52),
              backgroundColor: AppColors.brand,
            ),
            onPressed: _sending ? null : _submit,
            icon: _sending
                ? const SizedBox.square(
                    dimension: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.check_circle),
            label: Text(_sending ? 'Enviando...' : 'Confirmar reserva'),
          ),
        ],
      ),
    ),
  );
}
