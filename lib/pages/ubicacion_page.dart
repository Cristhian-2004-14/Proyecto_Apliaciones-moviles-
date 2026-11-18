import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../core/app_colors.dart';
import '../core/negocio_info.dart';
import '../widgets/clima_card.dart';
import '../widgets/info_card.dart';
import 'mapa_page.dart';

class UbicacionPage extends StatelessWidget {
  const UbicacionPage({super.key});

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
            NegocioInfo.nombre,
            style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
          ),
        ),
        const SizedBox(height: 24),
        const InfoCard(
          icon: Icons.place,
          title: 'Ubicación',
          text: NegocioInfo.direccion,
        ),
        const InfoCard(
          icon: Icons.schedule,
          title: 'Horarios',
          text: 'Lunes a domingo\n12:00 a 15:30 y 18:30 a 23:00',
        ),
        const InfoCard(
          icon: Icons.phone,
          title: 'Contacto',
          text: '+591 ${NegocioInfo.telefono}',
        ),
        const SizedBox(height: 14),
        const ClimaCard(),
        const SizedBox(height: 14),
        FilledButton.icon(
          style: FilledButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
            backgroundColor: AppColors.brand,
          ),
          onPressed: () => _open(
            context,
            'https://www.google.com/maps/search/?api=1&query=${NegocioInfo.latitud},${NegocioInfo.longitud}',
          ),
          icon: const Icon(Icons.directions),
          label: const Text('Cómo llegar'),
        ),
        const SizedBox(height: 10),
        OutlinedButton.icon(
          style: OutlinedButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
          ),
          onPressed: () => _open(context, 'tel:+591${NegocioInfo.telefono}'),
          icon: const Icon(Icons.phone),
          label: const Text('Llamar'),
        ),
        const SizedBox(height: 10),
        OutlinedButton.icon(
          style: OutlinedButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
          ),
          onPressed: () => _open(
            context,
            'https://wa.me/${NegocioInfo.whatsapp}?text=${Uri.encodeComponent('Hola, quisiera consultar sobre ${NegocioInfo.nombre}.')}',
          ),
          icon: const Icon(Icons.chat),
          label: const Text('Contactar por WhatsApp'),
        ),
        const SizedBox(height: 10),
        OutlinedButton.icon(
          style: OutlinedButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
          ),
          onPressed: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const MapaPage()),
          ),
          icon: const Icon(Icons.map_outlined),
          label: const Text('Ver mapa'),
        ),
      ],
    ),
  );
}
