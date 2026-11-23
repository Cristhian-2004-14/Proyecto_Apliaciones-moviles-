import 'package:flutter/foundation.dart';
import 'package:image_picker/image_picker.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

import '../models/negocio_configuracion.dart';

class FotoException implements Exception {
  const FotoException(this.message);
  final String message;

  @override
  String toString() => message;
}

class StorageService {
  static const negocioId = 'brasas-del-oriente';
  static const bucket = 'negocios';
  static const _maxBytes = 5 * 1024 * 1024;
  static final fotoVersion = ValueNotifier<int>(0);

  SupabaseClient get _client => Supabase.instance.client;

  Future<NegocioConfiguracion?> obtenerConfiguracion() async {
    final row = await _client
        .from('negocio_configuracion')
        .select('id, nombre, foto_path')
        .eq('id', negocioId)
        .maybeSingle();
    return row == null ? null : NegocioConfiguracion.fromMap(row);
  }

  String? urlPublica(String? fotoPath) {
    if (fotoPath == null || fotoPath.isEmpty) return null;
    return _client.storage.from(bucket).getPublicUrl(fotoPath);
  }

  Future<String> subirFoto(XFile image) async {
    final bytes = await image.readAsBytes();
    _validarImagen(image, bytes);
    final extension = _extension(image.name);
    final path = '$negocioId/portada.$extension';

    await _client.storage
        .from(bucket)
        .uploadBinary(
          path,
          bytes,
          fileOptions: FileOptions(
            cacheControl: '3600',
            upsert: true,
            contentType: _contentType(extension),
          ),
        );
    await _client.from('negocio_configuracion').upsert({
      'id': negocioId,
      'nombre': 'Brasas del Oriente',
      'foto_path': path,
      'updated_at': DateTime.now().toUtc().toIso8601String(),
    });
    fotoVersion.value++;
    return urlPublica(path)!;
  }

  Future<String> subirFotoProducto({
    required int productoId,
    required XFile image,
  }) async {
    final bytes = await image.readAsBytes();
    _validarImagen(image, bytes);
    final extension = _extension(image.name);
    final path = 'productos/$productoId/foto.$extension';

    await _client.storage
        .from(bucket)
        .uploadBinary(
          path,
          bytes,
          fileOptions: FileOptions(
            cacheControl: '3600',
            upsert: true,
            contentType: _contentType(extension),
          ),
        );
    await _client
        .from('negocios')
        .update({'imagen_path': path})
        .eq('id', productoId);
    fotoVersion.value++;
    return urlPublica(path)!;
  }

  void _validarImagen(XFile image, Uint8List bytes) {
    final extension = _extension(image.name);
    const permitidas = {'jpg', 'jpeg', 'png', 'webp'};
    if (!permitidas.contains(extension)) {
      throw const FotoException('Elige una imagen JPG, PNG o WEBP.');
    }
    if (bytes.isEmpty || bytes.length > _maxBytes) {
      throw const FotoException('La imagen debe pesar como máximo 5 MB.');
    }
  }

  String _extension(String filename) {
    final point = filename.lastIndexOf('.');
    return point == -1 ? '' : filename.substring(point + 1).toLowerCase();
  }

  String _contentType(String extension) => switch (extension) {
    'png' => 'image/png',
    'webp' => 'image/webp',
    _ => 'image/jpeg',
  };
}
