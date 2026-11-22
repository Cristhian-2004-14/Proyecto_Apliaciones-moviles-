import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';

import '../models/comprobante_ocr.dart';

class OcrService {
  Future<ComprobanteOcr> leerComprobante(String imagePath) async {
    final recognizer = TextRecognizer(script: TextRecognitionScript.latin);
    try {
      final recognized = await recognizer.processImage(
        InputImage.fromFilePath(imagePath),
      );
      return parseText(recognized.text);
    } finally {
      await recognizer.close();
    }
  }

  ComprobanteOcr parseText(String raw) {
    final normalized = _normalizar(raw);
    final monto = _extraerMonto(normalized);
    final fecha = _extraerFecha(normalized);
    return ComprobanteOcr(
      textoOriginal: raw,
      banco: normalized.contains('mercantil santa cruz')
          ? 'Banco Mercantil Santa Cruz'
          : null,
      exitoso:
          RegExp(
            r'(transferencia|transaccion|operacion)\s+exitosa',
          ).hasMatch(normalized)
          ? true
          : null,
      monto: monto,
      fechaOperacion: fecha,
      beneficiario: _extraerLineaDespuesDe(
        raw,
        RegExp(r'beneficiario|cuenta destino', caseSensitive: false),
      ),
      cuentaDestino: _extraerCuenta(normalized),
      codigoOperacion: _extraerCodigo(normalized),
    );
  }

  String _normalizar(String value) => value
      .toLowerCase()
      .replaceAll('á', 'a')
      .replaceAll('é', 'e')
      .replaceAll('í', 'i')
      .replaceAll('ó', 'o')
      .replaceAll('ú', 'u')
      .replaceAll(RegExp(r'\s+'), ' ');

  double? _extraerMonto(String text) {
    final match = RegExp(
      r'(?:importe|monto|bs\.?)[^0-9]{0,12}([0-9]{1,3}(?:[.,][0-9]{3})*[.,][0-9]{2})',
    ).firstMatch(text);
    final value = match?.group(1);
    if (value == null) return null;
    final normalized = value.contains(',') && value.contains('.')
        ? value.replaceAll('.', '').replaceAll(',', '.')
        : value.replaceAll(',', '.');
    return double.tryParse(normalized);
  }

  DateTime? _extraerFecha(String text) {
    final numeric = RegExp(
      r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b',
    ).firstMatch(text);
    if (numeric != null) {
      final year = int.parse(numeric.group(3)!);
      return DateTime(
        year < 100 ? 2000 + year : year,
        int.parse(numeric.group(2)!),
        int.parse(numeric.group(1)!),
      );
    }
    final textual = RegExp(
      r'\b(\d{1,2})\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+de\s+(\d{4})',
    ).firstMatch(text);
    if (textual == null) return null;
    const months = {
      'enero': 1,
      'febrero': 2,
      'marzo': 3,
      'abril': 4,
      'mayo': 5,
      'junio': 6,
      'julio': 7,
      'agosto': 8,
      'septiembre': 9,
      'octubre': 10,
      'noviembre': 11,
      'diciembre': 12,
    };
    return DateTime(
      int.parse(textual.group(3)!),
      months[textual.group(2)]!,
      int.parse(textual.group(1)!),
    );
  }

  String? _extraerCuenta(String text) {
    final match = RegExp(r'\b\d{4}[- ]?\d{4,12}\b').firstMatch(text);
    return match?.group(0)?.replaceAll(RegExp(r'[- ]'), '');
  }

  String? _extraerCodigo(String text) {
    final match = RegExp(
      r'(?:codigo(?: de operacion)?|nro\.? operacion|referencia)\s*[:#-]?\s*([a-z0-9-]{5,})',
    ).firstMatch(text);
    return match?.group(1)?.toUpperCase();
  }

  String? _extraerLineaDespuesDe(String text, RegExp marker) {
    final lines = text.split(RegExp(r'\r?\n'));
    for (var index = 0; index < lines.length - 1; index++) {
      if (marker.hasMatch(lines[index])) {
        final next = lines[index + 1].trim();
        if (next.isNotEmpty && next.length < 90) return next;
      }
    }
    return null;
  }
}
