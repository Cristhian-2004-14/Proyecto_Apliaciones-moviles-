import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../services/storage_service.dart';

class FotoNegocioPage extends StatefulWidget {
  const FotoNegocioPage({super.key});

  @override
  State<FotoNegocioPage> createState() => _FotoNegocioPageState();
}

class _FotoNegocioPageState extends State<FotoNegocioPage> {
  final _storage = StorageService();
  final _picker = ImagePicker();
  late Future<String?> _fotoFuture;
  XFile? _seleccionada;
  bool _subiendo = false;

  @override
  void initState() {
    super.initState();
    _fotoFuture = _cargarFoto();
  }

  Future<String?> _cargarFoto() async {
    final configuracion = await _storage.obtenerConfiguracion();
    return _storage.urlPublica(configuracion?.fotoPath);
  }

  Future<void> _seleccionarFoto() async {
    final image = await _picker.pickImage(
      source: ImageSource.gallery,
      maxWidth: 1600,
      imageQuality: 85,
    );
    if (image != null && mounted) setState(() => _seleccionada = image);
  }

  Future<void> _subirFoto() async {
    final image = _seleccionada;
    if (image == null) {
      _mensaje('Primero selecciona una foto de la galería.');
      return;
    }
    setState(() => _subiendo = true);
    try {
      await _storage.subirFoto(image);
      if (!mounted) return;
      setState(() {
        _seleccionada = null;
        _fotoFuture = _cargarFoto();
      });
      _mensaje('Foto actualizada correctamente.');
    } catch (error) {
      _mensaje('No se pudo subir la foto: $error');
    } finally {
      if (mounted) setState(() => _subiendo = false);
    }
  }

  void _mensaje(String text) =>
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(text)));

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Foto del negocio')),
    body: ListView(
      padding: const EdgeInsets.all(20),
      children: [
        Text(
          'Portada de Brasas del Oriente',
          style: Theme.of(context).textTheme.titleLarge,
        ),
        const SizedBox(height: 8),
        const Text('Solo el dueño puede actualizar esta imagen.'),
        const SizedBox(height: 20),
        FutureBuilder<String?>(
          future: _fotoFuture,
          builder: (context, snapshot) {
            final url = snapshot.data;
            return Container(
              height: 190,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(20),
                color: Theme.of(context).colorScheme.surfaceContainerHighest,
              ),
              clipBehavior: Clip.antiAlias,
              child: url == null
                  ? const Center(
                      child: Icon(Icons.storefront_outlined, size: 70),
                    )
                  : Image.network(
                      '$url?t=${DateTime.now().millisecondsSinceEpoch}',
                      fit: BoxFit.cover,
                      errorBuilder: (_, _, _) => const Center(
                        child: Text('No se pudo cargar la foto actual.'),
                      ),
                    ),
            );
          },
        ),
        if (_seleccionada != null) ...[
          const SizedBox(height: 18),
          Text(
            'Nueva foto seleccionada: ${_seleccionada!.name}',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
        ],
        const SizedBox(height: 24),
        OutlinedButton.icon(
          onPressed: _subiendo ? null : _seleccionarFoto,
          icon: const Icon(Icons.photo_library_outlined),
          label: const Text('Seleccionar foto'),
        ),
        const SizedBox(height: 12),
        FilledButton.icon(
          onPressed: _subiendo || _seleccionada == null ? null : _subirFoto,
          icon: _subiendo
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : const Icon(Icons.cloud_upload_outlined),
          label: Text(_subiendo ? 'Subiendo foto...' : 'Guardar foto'),
        ),
      ],
    ),
  );
}
