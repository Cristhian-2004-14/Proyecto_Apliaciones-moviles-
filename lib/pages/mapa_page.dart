import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../core/app_colors.dart';
import '../core/negocio_info.dart';

class MapaPage extends StatelessWidget {
  const MapaPage({super.key});

  @override
  Widget build(BuildContext context) {
    final punto = LatLng(NegocioInfo.latitud, NegocioInfo.longitud);
    return Scaffold(
      appBar: AppBar(title: const Text('Mapa del negocio')),
      body: Stack(
        children: [
          FlutterMap(
            options: MapOptions(initialCenter: punto, initialZoom: 15),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'bo.edu.upds.brasasdeloriente',
              ),
              MarkerLayer(
                markers: [
                  Marker(
                    point: punto,
                    width: 150,
                    height: 80,
                    child: const Column(
                      children: [
                        Icon(
                          Icons.location_on,
                          color: AppColors.brand,
                          size: 44,
                        ),
                        Text(
                          'Brasas del Oriente',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ],
          ),
          const Positioned(
            right: 10,
            bottom: 10,
            child: Card(
              child: Padding(
                padding: EdgeInsets.all(8),
                child: Text('© OpenStreetMap contributors'),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
