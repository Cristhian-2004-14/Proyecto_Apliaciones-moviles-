import 'package:conectacruz/models/pedido_historial.dart';
import 'package:conectacruz/models/reserva_resumen.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Estados de reserva', () {
    test('muestran etiquetas claras para el cliente', () {
      expect(EstadoReserva.solicitada.label, 'EN ESPERA');
      expect(EstadoReserva.aceptada.label, 'CONFIRMADA');
      expect(EstadoReserva.denegada.label, 'RECHAZADA');
    });

    test('interpreta los estados que vienen de Supabase', () {
      final reserva = ReservaResumen.fromMap({
        'id': 8,
        'nombre': 'Cliente de prueba',
        'telefono': '71234567',
        'fecha': '2026-11-30',
        'hora': '20:00:00',
        'personas': 4,
        'estado': 'aceptada',
      });

      expect(reserva.estado, EstadoReserva.aceptada);
      expect(reserva.estado.label, 'CONFIRMADA');
    });
  });

  group('Historial de pedidos', () {
    test('incluye un pago aprobado asociado al pedido', () {
      final pedido = PedidoHistorial.fromMap({
        'id': 12,
        'total': 100.0,
        'estado': 'confirmado',
        'created_at': '2026-11-23T12:00:00Z',
        'pagos': [
          {
            'id': 'pago-prueba',
            'pedido_id': 12,
            'monto_esperado': 100.0,
            'estado': 'pagado',
            'created_at': '2026-11-23T12:01:00Z',
            'qr_path': null,
            'beneficiario': null,
          },
        ],
      });

      expect(pedido.id, 12);
      expect(pedido.pago, isNotNull);
      expect(pedido.pago!.estado.label, 'PAGADO');
    });
  });
}
