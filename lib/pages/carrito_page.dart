import 'package:flutter/material.dart';

import '../core/app_colors.dart';
import '../services/carrito_controller.dart';
import 'pedido_page.dart';

class CarritoPage extends StatelessWidget {
  const CarritoPage({super.key, required this.carrito});

  final CarritoController carrito;

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Mi pedido')),
    body: AnimatedBuilder(
      animation: carrito,
      builder: (context, _) {
        if (carrito.estaVacio) {
          return const Center(
            child: Padding(
              padding: EdgeInsets.all(32),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.shopping_cart_outlined, size: 64),
                  SizedBox(height: 12),
                  Text('Tu carrito está vacío.'),
                  SizedBox(height: 4),
                  Text('Agrega productos desde el menú.'),
                ],
              ),
            ),
          );
        }

        return Column(
          children: [
            Expanded(
              child: ListView.separated(
                padding: const EdgeInsets.all(16),
                itemCount: carrito.items.length,
                separatorBuilder: (_, _) => const SizedBox(height: 8),
                itemBuilder: (context, index) {
                  final item = carrito.items[index];
                  return Card(
                    child: ListTile(
                      title: Text(item.producto.nombre),
                      subtitle: Text(
                        'Bs. ${item.producto.precio.toStringAsFixed(0)} c/u',
                      ),
                      leading: IconButton(
                        tooltip: 'Quitar uno',
                        onPressed: () => carrito.quitarUno(item.producto),
                        icon: const Icon(Icons.remove_circle_outline),
                      ),
                      trailing: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text('${item.cantidad}'),
                          IconButton(
                            tooltip: 'Agregar uno',
                            onPressed: () => carrito.agregar(item.producto),
                            icon: const Icon(Icons.add_circle_outline),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            SafeArea(
              top: false,
              child: Container(
                padding: const EdgeInsets.all(20),
                decoration: const BoxDecoration(
                  color: Colors.white,
                  boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 8)],
                ),
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text(
                          'Total',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        Text(
                          'Bs. ${carrito.total.toStringAsFixed(0)}',
                          style: const TextStyle(
                            color: AppColors.brand,
                            fontWeight: FontWeight.bold,
                            fontSize: 20,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    FilledButton.icon(
                      style: FilledButton.styleFrom(
                        minimumSize: const Size.fromHeight(52),
                        backgroundColor: AppColors.brand,
                      ),
                      onPressed: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => PedidoPage(carrito: carrito),
                        ),
                      ),
                      icon: const Icon(Icons.receipt_long),
                      label: const Text('Confirmar pedido'),
                    ),
                  ],
                ),
              ),
            ),
          ],
        );
      },
    ),
  );
}
