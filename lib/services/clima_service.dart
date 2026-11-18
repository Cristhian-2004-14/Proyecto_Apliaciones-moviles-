import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

import '../core/negocio_info.dart';
import '../models/clima.dart';

class ClimaService {
  ClimaService({http.Client? client}) : _client = client ?? http.Client();

  final http.Client _client;

  Future<Clima> obtenerClimaActual() async {
    final uri = Uri.https('api.open-meteo.com', '/v1/forecast', {
      'latitude': '${NegocioInfo.latitud}',
      'longitude': '${NegocioInfo.longitud}',
      'current': 'temperature_2m,weather_code',
      'timezone': 'America/La_Paz',
    });
    try {
      final response = await _client
          .get(uri)
          .timeout(const Duration(seconds: 10));
      if (response.statusCode != 200) {
        throw Exception('Open-Meteo respondió con ${response.statusCode}.');
      }
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return Clima.fromJson(data);
    } on TimeoutException {
      throw Exception('La consulta del clima tardó demasiado.');
    } on FormatException {
      throw Exception('La respuesta del clima no tiene el formato esperado.');
    }
  }
}
