import 'package:speech_to_text/speech_to_text.dart';

class VozException implements Exception {
  const VozException(this.message);
  final String message;

  @override
  String toString() => message;
}

class VozService {
  final SpeechToText _speech = SpeechToText();

  bool get estaEscuchando => _speech.isListening;

  Future<void> comenzar({
    required void Function(String texto, bool finalizado) onResultado,
    required void Function(String estado) onEstado,
    required void Function(String mensaje) onError,
  }) async {
    final disponible = await _speech.initialize(
      onStatus: onEstado,
      onError: (error) => onError(_mensajeError(error.errorMsg)),
    );
    if (!disponible) {
      throw const VozException(
        'No se pudo activar el micrófono. Revisa el permiso de audio.',
      );
    }
    await _speech.listen(
      onResult: (result) =>
          onResultado(result.recognizedWords, result.finalResult),
      listenOptions: SpeechListenOptions(listenMode: ListenMode.confirmation),
    );
  }

  Future<void> detener() => _speech.stop();

  void dispose() {
    _speech.stop();
  }

  String _mensajeError(String error) {
    if (error.contains('permission')) {
      return 'Se necesita permiso de micrófono para buscar por voz.';
    }
    if (error.contains('network')) {
      return 'No se pudo reconocer la voz. Revisa tu conexión a internet.';
    }
    return 'No se pudo reconocer la voz. Intenta nuevamente.';
  }
}
