import 'package:flutter/material.dart';

import '../core/app_colors.dart';
import '../services/carrito_controller.dart';
import '../services/storage_service.dart';
import '../widgets/access_card.dart';
import 'carrito_page.dart';
import 'cuenta_page.dart';
import 'catalogo_page.dart';
import 'consulta_page.dart';
import 'reserva_page.dart';
import 'ubicacion_page.dart';

class InicioPage extends StatelessWidget {
  const InicioPage({super.key, required this.carrito});

  final CarritoController carrito;

  @override
  Widget build(BuildContext context) => Scaffold(
    body: SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const _Banner(),
          const SizedBox(height: 24),
          Text(
            '¿Qué deseas hacer?',
            style: Theme.of(
              context,
            ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          AccessCard(
            icon: Icons.menu_book_rounded,
            title: 'Ver menú',
            subtitle: 'Parrilladas, cortes y más',
            onTap: () => _go(context, CatalogoPage(carrito: carrito)),
          ),
          AccessCard(
            icon: Icons.shopping_cart_outlined,
            title: 'Mi pedido',
            subtitle: 'Revisa productos y confirma tu orden',
            onTap: () => _go(context, CarritoPage(carrito: carrito)),
          ),
          AccessCard(
            icon: Icons.account_circle_outlined,
            title: 'Mi cuenta',
            subtitle: 'Ingresa como cliente o dueño',
            onTap: () => _go(context, const CuentaPage()),
          ),
          AccessCard(
            icon: Icons.calendar_month_rounded,
            title: 'Reservar mesa',
            subtitle: 'Solicita tu mesa en minutos',
            onTap: () => _go(context, const ReservaPage()),
          ),
          AccessCard(
            icon: Icons.chat_bubble_outline,
            title: 'Enviar consulta',
            subtitle: 'Resolvemos tus dudas',
            onTap: () => _go(context, const ConsultaPage()),
          ),
          AccessCard(
            icon: Icons.location_on_rounded,
            title: 'Ubicación y horarios',
            subtitle: 'Visítanos en Santa Cruz',
            onTap: () => _go(context, const UbicacionPage()),
          ),
          const SizedBox(height: 8),
          const Text(
            'Datos y precios demostrativos para fines académicos.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.black54, fontSize: 12),
          ),
        ],
      ),
    ),
  );

  void _go(BuildContext context, Widget page) =>
      Navigator.push(context, MaterialPageRoute(builder: (_) => page));
}

class _Banner extends StatefulWidget {
  const _Banner();

  @override
  State<_Banner> createState() => _BannerState();
}

class _BannerState extends State<_Banner> {
  final _storage = StorageService();
  late Future<String?> _fotoFuture;

  @override
  void initState() {
    super.initState();
    _fotoFuture = _obtenerFoto();
    StorageService.fotoVersion.addListener(_recargarFoto);
  }

  @override
  void dispose() {
    StorageService.fotoVersion.removeListener(_recargarFoto);
    super.dispose();
  }

  void _recargarFoto() {
    if (mounted) setState(() => _fotoFuture = _obtenerFoto());
  }

  Future<String?> _obtenerFoto() async {
    try {
      final config = await _storage.obtenerConfiguracion();
      return _storage.urlPublica(config?.fotoPath);
    } catch (_) {
      return null;
    }
  }

  @override
  Widget build(BuildContext context) => FutureBuilder<String?>(
    future: _fotoFuture,
    builder: (context, snapshot) {
      final fotoUrl = snapshot.data;
      return Container(
        height: 176,
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(24),
          gradient: const LinearGradient(
            colors: [AppColors.coal, Color(0xFF563024), AppColors.brand],
          ),
          image: fotoUrl == null
              ? null
              : DecorationImage(
                  image: NetworkImage(fotoUrl),
                  fit: BoxFit.cover,
                  colorFilter: ColorFilter.mode(
                    Colors.black.withValues(alpha: 0.52),
                    BlendMode.darken,
                  ),
                ),
        ),
        child: const Row(
          children: [
            Expanded(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Brasas del Oriente',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 27,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Parrilla, tradición y sabor cruceño.',
                    style: TextStyle(color: Colors.white70, fontSize: 16),
                  ),
                ],
              ),
            ),
            Icon(Icons.outdoor_grill, color: AppColors.gold, size: 70),
          ],
        ),
      );
    },
  );
}
