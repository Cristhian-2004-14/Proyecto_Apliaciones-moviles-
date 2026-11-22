class ConfiguracionQr {
  const ConfiguracionQr({
    required this.id,
    required this.qrPath,
    required this.beneficiario,
    this.cuentaDestino,
    required this.activo,
  });

  final String id;
  final String qrPath;
  final String beneficiario;
  final String? cuentaDestino;
  final bool activo;

  factory ConfiguracionQr.fromMap(Map<String, dynamic> map) => ConfiguracionQr(
    id: map['id'].toString(),
    qrPath: map['qr_path'] as String,
    beneficiario: map['beneficiario'] as String,
    cuentaDestino: map['cuenta_destino'] as String?,
    activo: map['activo'] as bool? ?? false,
  );
}
