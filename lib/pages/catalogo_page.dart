import 'package:flutter/material.dart';

import '../config/supabase_config.dart';
import '../models/negocio.dart';
import '../services/negocio_service.dart';
import '../widgets/negocio_card.dart';

class CatalogoPage extends StatefulWidget {
  const CatalogoPage({super.key});

  @override
  State<CatalogoPage> createState() => _CatalogoPageState();
}

class _CatalogoPageState extends State<CatalogoPage> {
  final _service = NegocioService();
  late Future<List<Negocio>> _future;
  String _rubro = 'Todos';
  String _search = '';

  @override
  void initState() {
    super.initState();
    _future = _service.obtenerNegocios();
  }

  void _retry() => setState(() => _future = _service.obtenerNegocios());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Menú digital')),
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
                        decoration: const InputDecoration(
                          prefixIcon: Icon(Icons.search),
                          labelText: 'Buscar en el menú',
                        ),
                        onChanged: (value) => setState(() => _search = value),
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
                              itemBuilder: (_, index) =>
                                  NegocioCard(negocio: items[index]),
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
