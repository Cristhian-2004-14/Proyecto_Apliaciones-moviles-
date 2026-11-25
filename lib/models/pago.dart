enum EstadoPago {
  pendiente,
  enValidacion,
  comprobanteValidado,
  revisionManual,
  rechazado,
  pagado;

  String get dbValue => switch (this) {
    EstadoPago.pendiente => 'pendiente',
    EstadoPago.enValidacion => 'en_validacion',
    EstadoPago.comprobanteValidado => 'comprobante_validado',
    EstadoPago.revisionManual => 'revision_manual',
    EstadoPago.rechazado => 'rechazado',
    EstadoPago.pagado => 'pagado',
  };

  String get label => switch (this) {
    EstadoPago.pendiente => 'PENDIENTE',
    EstadoPago.enValidacion => 'EN VALIDACIÓN',
    EstadoPago.comprobanteValidado => 'COMPROBANTE VALIDADO',
    EstadoPago.revisionManual => 'REVISIÓN MANUAL',
    EstadoPago.rechazado => 'RECHAZADO',
    EstadoPago.pagado => 'PAGADO',
  };

  static EstadoPago fromDb(String value) => EstadoPago.values.firstWhere(
    (estado) => estado.dbValue == value,
    orElse: () => EstadoPago.revisionManual,
  );
}

class Pago {
  const Pago({
    required this.id,
    required this.pedidoId,
    required this.montoEsperado,
    required this.estado,
    required this.createdAt,
    this.qrPath,
    this.beneficiario,
  });

  final String id;
  final int pedidoId;
  final double montoEsperado;
  final EstadoPago estado;
  final DateTime createdAt;
  final String? qrPath;
  final String? beneficiario;

  factory Pago.fromMap(Map<String, dynamic> map) => Pago(
    id: map['id'].toString(),
    pedidoId: (map['pedido_id'] as num).toInt(),
    montoEsperado: (map['monto_esperado'] as num).toDouble(),
    estado: EstadoPago.fromDb(map['estado'] as String),
    createdAt: DateTime.parse(map['created_at'] as String).toLocal(),
    qrPath: map['qr_path'] as String?,
    beneficiario: map['beneficiario'] as String?,
  );
}

class PagoAdmin extends Pago {
  const PagoAdmin({
    required super.id,
    required super.pedidoId,
    required super.montoEsperado,
    required super.estado,
    required super.createdAt,
    this.cliente,
    this.telefono,
    this.beneficiarioEsperado,
    this.cuentaDestinoEsperada,
  });

  final String? cliente;
  final String? telefono;
  final String? beneficiarioEsperado;
  final String? cuentaDestinoEsperada;

  factory PagoAdmin.fromMap(Map<String, dynamic> map) {
    final pedido = map['pedidos'] as Map<String, dynamic>?;
    final configuracion = map['configuracion_qr_pago'] as Map<String, dynamic>?;
    return PagoAdmin(
      id: map['id'].toString(),
      pedidoId: (map['pedido_id'] as num).toInt(),
      montoEsperado: (map['monto_esperado'] as num).toDouble(),
      estado: EstadoPago.fromDb(map['estado'] as String),
      createdAt: DateTime.parse(map['created_at'] as String).toLocal(),
      cliente: pedido?['nombre'] as String?,
      telefono: pedido?['telefono'] as String?,
      beneficiarioEsperado: configuracion?['beneficiario'] as String?,
      cuentaDestinoEsperada: configuracion?['cuenta_destino'] as String?,
    );
  }
}
