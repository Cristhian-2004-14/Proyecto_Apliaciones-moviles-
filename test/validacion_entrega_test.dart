import 'package:conectacruz/core/validators.dart';
import 'package:conectacruz/models/configuracion_qr.dart';
import 'package:conectacruz/models/pedido_historial.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('interpreta una configuración QR activa del negocio', () {
    final configuracion = ConfiguracionQr.fromMap({
      'id': 'qr-activo',
      'qr_path': 'pagos_qr/qr.png',
      'beneficiario': 'Beneficiario autorizado',
      'cuenta_destino': '00000000',
      'activo': true,
    });

    expect(configuracion.activo, isTrue);
    expect(configuracion.qrPath, 'pagos_qr/qr.png');
  });

  test('una configuración QR sin estado activo queda deshabilitada', () {
    final configuracion = ConfiguracionQr.fromMap({
      'id': 'qr-inactivo',
      'qr_path': 'pagos_qr/qr.png',
      'beneficiario': 'Beneficiario autorizado',
    });

    expect(configuracion.activo, isFalse);
  });

  test('un pedido sin pago asociado se conserva como pago no iniciado', () {
    final pedido = PedidoHistorial.fromMap({
      'id': 18,
      'total': 84.0,
      'estado': 'pendiente',
      'created_at': '2026-11-23T12:00:00Z',
      'pagos': <Map<String, dynamic>>[],
    });

    expect(pedido.pago, isNull);
    expect(pedido.estado, 'pendiente');
  });

  test('los formularios rechazan nombres y mensajes incompletos', () {
    expect(Validators.requiredName('   '), isNotNull);
    expect(Validators.message('Corto'), isNotNull);
    expect(Validators.message('Consulta con información válida'), isNull);
  });
}
