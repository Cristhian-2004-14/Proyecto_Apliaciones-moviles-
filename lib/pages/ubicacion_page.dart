import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../core/app_colors.dart';
import '../widgets/info_card.dart';

class UbicacionPage extends StatelessWidget {
  const UbicacionPage({super.key});

  static const _address = 'Av. Ejemplo 123, Santa Cruz de la Sierra, Bolivia';

  Future<void> _open(BuildContext context, String url) async {
    if (!await launchUrl(
          Uri.parse(url),
          mode: LaunchMode.externalApplication,
        ) &&
        context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No se pudo abrir la aplicación externa.'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Ubicación y horarios')),
    body: ListView(
      padding: const EdgeInsets.all(20),
      children: [
        const Icon(Icons.location_on, size: 62, color: AppColors.brand),
        const SizedBox(height: 10),
        const Center(
          child: Text(
            'Brasas del Oriente',
            style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
          ),
        ),
        const SizedBox(height: 24),
        const InfoCard(
          icon: Icons.place,
          title: 'Dirección demostrativa',
          text: _address,
        ),
        const InfoCard(
          icon: Icons.schedule,
          title: 'Horarios demostrativos',
          text: 'Lunes a domingo\n12:00 a 15:30 y 18:30 a 23:00',
        ),
        const InfoCard(
          icon: Icons.phone,
          title: 'Contacto demostrativo',
          text: '+591 70000000',
        ),
        const SizedBox(height: 14),
        FilledButton.icon(
          style: FilledButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
            backgroundColor: AppColors.brand,
          ),
          onPressed: () => _open(
            context,
            'https://www.google.com/maps/search/?api=1&query=${Uri.encodeComponent(_address)}',
          ),
          icon: const Icon(Icons.directions),
          label: const Text('Cómo llegar'),
        ),
        const SizedBox(height: 10),
        OutlinedButton.icon(
          style: OutlinedButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
          ),
          onPressed: () => _open(
            context,
            'https://wa.me/59170000000?text=${Uri.encodeComponent('Hola, quisiera consultar sobre Brasas del Oriente.')}',
          ),
          icon: const Icon(Icons.chat),
          label: const Text('Contactar por WhatsApp'),
        ),
      ],
    ),
  );
}
