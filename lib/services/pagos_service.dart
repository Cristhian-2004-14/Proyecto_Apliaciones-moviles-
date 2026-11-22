import 'dart:typed_data';

import 'package:crypto/crypto.dart';
import 'package:http/http.dart' as http;
import 'package:image_gallery_saver_plus/image_gallery_saver_plus.dart';
import 'package:image_picker/image_picker.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

import '../models/comprobante_ocr.dart';
import '../models/configuracion_qr.dart';
import '../models/pago.dart';
import 'ocr_service.dart';

class PagoException implements Exception {
  const PagoException(this.message);
  final String message;

  @override
  String toString() => message;
}

class PagosService {
  static const qrBucket = 'pagos_qr';
  static const comprobantesBucket = 'comprobantes_pago';
  static const _maxBytes = 5 * 1024 * 1024;

  final OcrService _ocr;

  PagosService({OcrService? ocr}) : _ocr = ocr ?? OcrService();

  SupabaseClient get _client => Supabase.instance.client;

  Future<Pago> crearParaPedido(int pedidoId) async {
    final response = await _client.rpc(
      'crear_pago_para_pedido',
      params: {'p_pedido_id': pedidoId},
    );
    return Pago.fromMap(Map<String, dynamic>.from(response as Map));
  }

  Future<ConfiguracionQr?> obtenerQrActivo() async {
    final response = await _client.rpc('obtener_qr_pago_activo');
    if (response == null) return null;
    return ConfiguracionQr.fromMap(Map<String, dynamic>.from(response as Map));
  }

  String urlQr(String qrPath) =>
      _client.storage.from(qrBucket).getPublicUrl(qrPath);

  Future<bool> descargarQr(String qrPath) async {
    final response = await http.get(Uri.parse(urlQr(qrPath)));
    if (response.statusCode != 200) return false;
    final result = await ImageGallerySaverPlus.saveImage(
      Uint8List.fromList(response.bodyBytes),
      quality: 100,
      name: 'qr_brasas_del_oriente',
    );
    return result is Map && result['isSuccess'] == true;
  }

  Future<Pago> cargarComprobante({
    required Pago pago,
    required XFile image,
  }) async {
    final bytes = await image.readAsBytes();
    final extension = _validarImagen(image.name, bytes);
    final hash = sha256.convert(bytes).toString();
    final lectura = await _ocr.leerComprobante(image.path);
    final timestamp = DateTime.now().toUtc().millisecondsSinceEpoch;
    final path = '${pago.id}/${timestamp}_${hash.substring(0, 12)}.$extension';

    await _client.storage
        .from(comprobantesBucket)
        .uploadBinary(
          path,
          bytes,
          fileOptions: FileOptions(
            cacheControl: '0',
            upsert: false,
            contentType: extension == 'png' ? 'image/png' : 'image/jpeg',
          ),
        );

    final response = await _client.rpc(
      'registrar_comprobante_pago',
      params: {
        'p_pago_id': pago.id,
        'p_ruta': path,
        'p_hash_sha256': hash,
        'p_texto_ocr': lectura.textoOriginal,
        'p_banco': lectura.banco,
        'p_exitoso': lectura.exitoso,
        'p_monto': lectura.monto,
        'p_fecha': lectura.fechaOperacion == null
            ? null
            : _dateOnly(lectura.fechaOperacion!),
        'p_beneficiario': lectura.beneficiario,
        'p_cuenta_destino': lectura.cuentaDestino,
        'p_codigo_operacion': lectura.codigoOperacion,
      },
    );
    return Pago.fromMap(Map<String, dynamic>.from(response as Map));
  }

  Future<void> guardarConfiguracionQr({
    required XFile image,
    required String beneficiario,
    required String cuentaDestino,
  }) async {
    final bytes = await image.readAsBytes();
    final extension = _validarImagen(image.name, bytes);
    if (beneficiario.trim().isEmpty || cuentaDestino.trim().isEmpty) {
      throw const PagoException('Completa beneficiario y cuenta de destino.');
    }
    final path =
        'configuracion/${DateTime.now().toUtc().millisecondsSinceEpoch}.$extension';
    await _client.storage
        .from(qrBucket)
        .uploadBinary(
          path,
          bytes,
          fileOptions: FileOptions(
            upsert: false,
            contentType: extension == 'png' ? 'image/png' : 'image/jpeg',
          ),
        );
    await _client
        .from('configuracion_qr_pago')
        .update({'activo': false})
        .eq('activo', true);
    await _client.from('configuracion_qr_pago').insert({
      'qr_path': path,
      'beneficiario': beneficiario.trim(),
      'cuenta_destino': cuentaDestino.trim(),
      'activo': true,
      'updated_at': DateTime.now().toUtc().toIso8601String(),
    });
  }

  Future<List<PagoAdmin>> obtenerPagosAdmin() async {
    final rows = await _client
        .from('pagos')
        .select(
          'id,pedido_id,monto_esperado,estado,created_at,pedidos(nombre,telefono)',
        )
        .order('created_at', ascending: false);
    return (rows as List)
        .cast<Map<String, dynamic>>()
        .map(PagoAdmin.fromMap)
        .toList();
  }

  Future<List<ComprobantePago>> obtenerComprobantes(String pagoId) async {
    final rows = await _client
        .from('comprobantes_pago')
        .select()
        .eq('pago_id', pagoId)
        .order('created_at', ascending: false);
    return (rows as List)
        .cast<Map<String, dynamic>>()
        .map(ComprobantePago.fromMap)
        .toList();
  }

  Future<String> urlComprobanteFirmada(String ruta) =>
      _client.storage.from(comprobantesBucket).createSignedUrl(ruta, 120);

  Future<void> resolverComoDueno({
    required String pagoId,
    required bool aprobar,
    required String observaciones,
    required String referenciaConstatacion,
  }) => _client.rpc(
    'resolver_pago_administrador',
    params: {
      'p_pago_id': pagoId,
      'p_aprobar': aprobar,
      'p_observaciones': observaciones.trim(),
      'p_referencia_constatacion': referenciaConstatacion.trim(),
    },
  );

  String _validarImagen(String name, Uint8List bytes) {
    if (bytes.isEmpty || bytes.length > _maxBytes) {
      throw const PagoException('El comprobante debe pesar como máximo 5 MB.');
    }
    final isPng =
        bytes.length >= 8 &&
        bytes[0] == 0x89 &&
        bytes[1] == 0x50 &&
        bytes[2] == 0x4E &&
        bytes[3] == 0x47;
    final isJpeg =
        bytes.length >= 3 &&
        bytes[0] == 0xFF &&
        bytes[1] == 0xD8 &&
        bytes[2] == 0xFF;
    if (!isPng && !isJpeg) {
      throw const PagoException(
        'Solo se permiten comprobantes JPG o PNG reales.',
      );
    }
    return isPng ? 'png' : 'jpg';
  }

  String _dateOnly(DateTime value) =>
      '${value.year.toString().padLeft(4, '0')}-${value.month.toString().padLeft(2, '0')}-${value.day.toString().padLeft(2, '0')}';
}
