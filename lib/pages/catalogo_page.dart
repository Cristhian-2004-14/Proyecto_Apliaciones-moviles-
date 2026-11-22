import 'package:flutter/material.dart';

import '../config/supabase_config.dart';
import '../models/negocio.dart';
import '../services/carrito_controller.dart';
import '../services/negocio_service.dart';
import '../services/voz_service.dart';
import '../widgets/negocio_card.dart';
import 'carrito_page.dart';

class CatalogoPage extends StatefulWidget {
  const CatalogoPage({super.key, required this.carrito});

  final CarritoController carrito;

  @override
  State<CatalogoPage> createState() => _CatalogoPageState();
}

class _CatalogoPageState extends State<CatalogoPage> {
  final _service = NegocioService();
  final _voz = VozService();
  final _searchController = TextEditingController();
  late Future<List<Negocio>> _future;
  String _rubro = 'Todos';
  String _search = '';
  String _textoReconocido = '';
  bool _escuchando = false;

  @override
  void initState() {
    super.initState();
    _future = _service.obtenerNegocios();
  }

  @override
  void dispose() {
    _voz.dispose();
    _searchController.dispose();
    super.dispose();
  }

  void _retry() => setState(() => _future = _service.obtenerNegocios());

  Future<void> _alternarVoz() async {
    if (_escuchando) {
      await _voz.detener();
      if (mounted) setState(() => _escuchando = false);
      return;
    }
    try {
      await _voz.comenzar(
        onResultado: (texto, finalizado) {
          if (!mounted) return;
          setState(() {
            _textoReconocido = texto;
            _search = texto;
            _searchController.value = TextEditingValue(
              text: texto,
              selection: TextSelection.collapsed(offset: texto.length),
            );
            if (finalizado) _escuchando = false;
          });
        },
        onEstado: (estado) {
          if (!mounted) return;
          if (estado == 'listening') {
            setState(() => _escuchando = true);
          } else if (estado == 'done' || estado == 'notListening') {
            setState(() => _escuchando = false);
          }
        },
        onError: _mostrarErrorVoz,
      );
      if (mounted) setState(() => _escuchando = _voz.estaEscuchando);
    } catch (error) {
      _mostrarErrorVoz(error.toString());
    }
  }

  void _mostrarErrorVoz(String mensaje) {
    if (!mounted) return;
    setState(() => _escuchando = false);
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text(mensaje)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Menú digital'),
        actions: [
          AnimatedBuilder(
            animation: widget.carrito,
            builder: (context, _) => IconButton(
              tooltip: 'Ver pedido',
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => CarritoPage(carrito: widget.carrito),
                ),
              ),
              icon: Badge(
                isLabelVisible: widget.carrito.cantidadTotal > 0,
                label: Text('${widget.carrito.cantidadTotal}'),
                child: const Icon(Icons.shopping_cart_outlined),
              ),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: FutureBuilder<List<Negocio>>(
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
                          const Icon(Icons.cloud_off, size: 48),
                          const SizedBox(height: 12),
                          const Text(
                            'No se pudo cargar el catálogo.',
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
                final negocios = snapshot.data ?? [];
                final rubros = [
                  'Todos',
                  ...{for (final negocio in negocios) negocio.rubro},
                ];
                final items = negocios.where((negocio) {
                  final matchesRubro =
                      _rubro == 'Todos' || negocio.rubro == _rubro;
                  final query = _search.toLowerCase().trim();
                  final matchesSearch =
                      query.isEmpty ||
                      negocio.nombre.toLowerCase().contains(query) ||
                      negocio.descripcion.toLowerCase().contains(query);
                  return matchesRubro && matchesSearch;
                }).toList();
                return Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
                      child: TextField(
                        controller: _searchController,
                        decoration: InputDecoration(
                          prefixIcon: Icon(Icons.search),
                          labelText: 'Buscar en el menú',
                          suffixIcon: IconButton(
                            tooltip: _escuchando
                                ? 'Detener búsqueda por voz'
                                : 'Buscar por voz',
                            onPressed: _alternarVoz,
                            icon: Icon(
                              _escuchando ? Icons.stop_circle : Icons.mic,
                              color: _escuchando
                                  ? Theme.of(context).colorScheme.error
                                  : null,
                            ),
                          ),
                        ),
                        onChanged: (value) => setState(() => _search = value),
                      ),
                    ),
                    if (_escuchando || _textoReconocido.isNotEmpty)
                      Padding(
                        padding: const EdgeInsets.fromLTRB(16, 2, 16, 6),
                        child: Row(
                          children: [
                            Icon(
                              _escuchando ? Icons.graphic_eq : Icons.mic_none,
                              size: 18,
                            ),
                            const SizedBox(width: 8),
                            Expanded(
                              child: Text(
                                _escuchando
                                    ? 'Escuchando...'
                                    : 'Reconocido: “$_textoReconocido”',
                              ),
                            ),
                          ],
                        ),
                      ),
                    if (!SupabaseConfig.isConfigured)
                      const Padding(
                        padding: EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 4,
                        ),
                        child: Text(
                          'Mostrando datos locales hasta configurar Supabase.',
                          textAlign: TextAlign.center,
                          style: TextStyle(fontSize: 12),
                        ),
                      ),
                    SizedBox(
                      height: 46,
                      child: ListView(
                        scrollDirection: Axis.horizontal,
                        padding: const EdgeInsets.symmetric(horizontal: 12),
                        children: rubros
                            .map(
                              (rubro) => Padding(
                                padding: const EdgeInsets.symmetric(
                                  horizontal: 4,
                                ),
                                child: ChoiceChip(
                                  label: Text(rubro),
                                  selected: rubro == _rubro,
                                  onSelected: (_) =>
                                      setState(() => _rubro = rubro),
                                ),
                              ),
                            )
                            .toList(),
                      ),
                    ),
                    Expanded(
                      child: items.isEmpty
                          ? const Center(
                              child: Text(
                                'No hay elementos que coincidan con tu búsqueda.',
                              ),
                            )
                          : ListView.builder(
                              padding: const EdgeInsets.all(16),
                              itemCount: items.length,
                              itemBuilder: (_, index) => NegocioCard(
                                negocio: items[index],
                                onAdd: () {
                                  widget.carrito.agregar(items[index]);
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(
                                      content: Text(
                                        '${items[index].nombre} agregado al pedido.',
                                      ),
                                    ),
                                  );
                                },
                              ),
                            ),
                    ),
                  ],
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
