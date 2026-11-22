class ComprobanteOcr {
  const ComprobanteOcr({
    required this.textoOriginal,
    this.banco,
    this.exitoso,
    this.monto,
    this.fechaOperacion,
    this.beneficiario,
    this.cuentaDestino,
    this.codigoOperacion,
  });

  final String textoOriginal;
  final String? banco;
  final bool? exitoso;
  final double? monto;
  final DateTime? fechaOperacion;
  final String? beneficiario;
  final String? cuentaDestino;
  final String? codigoOperacion;

  bool get tieneDatosBasicos =>
      banco != null &&
      exitoso != null &&
      monto != null &&
      fechaOperacion != null;
}

class ComprobantePago {
  const ComprobantePago({
    required this.id,
    required this.pagoId,
    required this.ruta,
    required this.createdAt,
    this.banco,
    this.monto,
    this.codigoOperacion,
    this.validacion,
  });

  final String id;
  final String pagoId;
  final String ruta;
  final DateTime createdAt;
  final String? banco;
  final double? monto;
  final String? codigoOperacion;
  final Map<String, dynamic>? validacion;

  factory ComprobantePago.fromMap(Map<String, dynamic> map) => ComprobantePago(
    id: map['id'].toString(),
    pagoId: map['pago_id'].toString(),
    ruta: map['ruta'] as String,
    createdAt: DateTime.parse(map['created_at'] as String).toLocal(),
    banco: map['banco_detectado'] as String?,
    monto: (map['monto_detectado'] as num?)?.toDouble(),
    codigoOperacion: map['codigo_operacion'] as String?,
    validacion: map['validacion'] as Map<String, dynamic>?,
  );
}
