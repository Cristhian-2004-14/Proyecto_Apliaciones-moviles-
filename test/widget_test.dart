import 'package:conectacruz/main.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('la bienvenida lleva al inicio de la churrasquería', (
    tester,
  ) async {
    await tester.pumpWidget(const ConectaCruzApp());
    expect(find.text('Brasas del Oriente'), findsOneWidget);
    await tester.tap(find.text('Entrar a la churrasquería'));
    await tester.pumpAndSettle();
    expect(find.text('¿Qué deseas hacer?'), findsOneWidget);
    expect(find.text('Reservar mesa'), findsOneWidget);
  });
}
