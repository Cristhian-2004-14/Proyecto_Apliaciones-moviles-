import 'pago.dart';

class PedidoHistorial {
  const PedidoHistorial({
    required this.id,
    required this.total,
    required this.estado,
    required this.fecha,
    this.pago,
  });

  final int id;
  final double total;
  final String estado;
  final DateTime fecha;
  final Pago? pago;

  factory PedidoHistorial.fromMap(Map<String, dynamic> map) {
    final pagos = map['pagos'];
    final pagoMap = pagos is List && pagos.isNotEmpty
        ? pagos.first as Map<String, dynamic>
        : pagos is Map<String, dynamic>
        ? pagos
        : null;
    return PedidoHistorial(
      id: (map['id'] as num).toInt(),
      total: (map['total'] as num).toDouble(),
      estado: map['estado'] as String,
      fecha: DateTime.parse(map['created_at'] as String).toLocal(),
      pago: pagoMap == null ? null : Pago.fromMap(pagoMap),
    );
  }
}
