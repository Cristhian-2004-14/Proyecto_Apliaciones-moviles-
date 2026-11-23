import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../models/negocio.dart';
import '../services/negocio_service.dart';
import '../services/storage_service.dart';

class FotosProductosPage extends StatefulWidget {
  const FotosProductosPage({super.key});

  @override
  State<FotosProductosPage> createState() => _FotosProductosPageState();
}

class _FotosProductosPageState extends State<FotosProductosPage> {
  final _negocios = NegocioService();
  final _storage = StorageService();
  final _picker = ImagePicker();
  late Future<List<Negocio>> _productosFuture;
  int? _subiendoId;

  @override
  void initState() {
    super.initState();
    _productosFuture = _negocios.obtenerNegocios();
  }

  Future<void> _cambiarFoto(Negocio producto) async {
    final image = await _picker.pickImage(
      source: ImageSource.gallery,
      maxWidth: 1600,
      imageQuality: 85,
    );
    if (image == null || !mounted) return;

    setState(() => _subiendoId = producto.id);
    try {
      await _storage.subirFotoProducto(productoId: producto.id, image: image);
      if (!mounted) return;
      setState(() => _productosFuture = _negocios.obtenerNegocios());
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Foto de ${producto.nombre} actualizada.')),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('No se pudo subir la foto: $error')),
      );
    } finally {
      if (mounted) setState(() => _subiendoId = null);
    }
  }

  Widget _miniatura(Negocio producto) {
    final url = _storage.urlPublica(producto.imagenPath);
    if (url == null) return CircleAvatar(child: Icon(producto.icono));
    return ClipRRect(
      borderRadius: BorderRadius.circular(10),
      child: Image.network(
        '$url?t=${DateTime.now().millisecondsSinceEpoch}',
        width: 58,
        height: 58,
        fit: BoxFit.cover,
        errorBuilder: (_, _, _) => CircleAvatar(child: Icon(producto.icono)),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Fotos de productos')),
    body: FutureBuilder<List<Negocio>>(
      future: _productosFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError) {
          return Center(
            child: FilledButton(
              onPressed: () => setState(
                () => _productosFuture = _negocios.obtenerNegocios(),
              ),
              child: const Text('Reintentar'),
            ),
          );
        }
        final productos = snapshot.data ?? [];
        return ListView(
          padding: const EdgeInsets.all(16),
          children: [
            Text(
              'Catálogo con fotos reales',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 6),
            const Text(
              'Selecciona cada producto para cargar o reemplazar su foto. '
              'Solo el dueño puede realizar este cambio.',
            ),
            const SizedBox(height: 16),
            ...productos.map(
              (producto) => Card(
                child: ListTile(
                  contentPadding: const EdgeInsets.all(12),
                  leading: _miniatura(producto),
                  title: Text(producto.nombre),
                  subtitle: Text(
                    producto.imagenPath == null
                        ? 'Aún no tiene foto'
                        : 'Foto cargada',
                  ),
                  trailing: _subiendoId == producto.id
                      ? const SizedBox(
                          width: 24,
                          height: 24,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : IconButton(
                          tooltip: 'Cambiar foto',
                          icon: const Icon(Icons.add_a_photo_outlined),
                          onPressed: _subiendoId == null
                              ? () => _cambiarFoto(producto)
                              : null,
                        ),
                ),
              ),
            ),
          ],
        );
      },
    ),
  );
}
