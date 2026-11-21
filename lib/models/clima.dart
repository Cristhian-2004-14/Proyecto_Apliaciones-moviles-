class Clima {
  const Clima({
    required this.temperatura,
    required this.codigoClima,
    required this.hora,
  });

  final double temperatura;
  final int codigoClima;
  final String hora;

  factory Clima.fromJson(Map<String, dynamic> json) {
    final current = json['current'] as Map<String, dynamic>;
    return Clima(
      temperatura: (current['temperature_2m'] as num).toDouble(),
      codigoClima: current['weather_code'] as int,
      hora: current['time'] as String,
    );
  }

  String get descripcion => switch (codigoClima) {
    0 => 'Despejado',
    1 || 2 => 'Parcialmente nublado',
    3 => 'Nublado',
    45 || 48 => 'Neblina',
    51 || 53 || 55 || 56 || 57 => 'Llovizna',
    61 || 63 || 65 || 66 || 67 || 80 || 81 || 82 => 'Lluvia',
    71 || 73 || 75 || 77 || 85 || 86 => 'Nieve',
    95 || 96 || 99 => 'Tormenta',
    _ => 'Condición no disponible',
  };
}
