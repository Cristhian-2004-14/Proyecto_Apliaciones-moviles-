import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

const brand = Color(0xFFD06A2A),
    coal = Color(0xFF201714),
    cream = Color(0xFFFFF7EF);
void main() => runApp(const ConectaCruzApp());

class ConectaCruzApp extends StatelessWidget {
  const ConectaCruzApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Brasas del Oriente',
    debugShowCheckedModeBanner: false,
    theme: ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(seedColor: brand),
      scaffoldBackgroundColor: cream,
      appBarTheme: const AppBarTheme(
        backgroundColor: coal,
        foregroundColor: Colors.white,
      ),
    ),
    home: const WelcomeScreen(),
  );
}

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});
  @override
  Widget build(BuildContext context) => Scaffold(
    body: SafeArea(
      child: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.outdoor_grill, color: brand, size: 88),
              const SizedBox(height: 20),
              Text(
                'Brasas del Oriente',
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                  color: coal,
                  fontWeight: FontWeight.w800,
                ),
              ),
              const SizedBox(height: 10),
              const Text(
                'El sabor de la parrilla cruceña, cerca de ti.',
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              FilledButton.icon(
                style: FilledButton.styleFrom(
                  minimumSize: const Size.fromHeight(54),
                  backgroundColor: brand,
                ),
                onPressed: () => Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (_) => const HomeScreen()),
                ),
                icon: const Icon(Icons.restaurant_menu),
                label: const Text('Entrar a la churrasquería'),
              ),
            ],
          ),
        ),
      ),
    ),
  );
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});
  @override
  Widget build(BuildContext context) => Scaffold(
    body: SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const _Banner(),
          const SizedBox(height: 24),
          Text(
            '¿Qué deseas hacer?',
            style: Theme.of(
              context,
            ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          _Access(
            Icons.menu_book_rounded,
            'Ver menú',
            'Parrilladas, cortes y más',
            () => _go(context, const MenuScreen()),
          ),
          _Access(
            Icons.calendar_month_rounded,
            'Reservar mesa',
            'Solicita tu mesa en minutos',
            () => _go(context, const ReservationScreen()),
          ),
          _Access(
            Icons.location_on_rounded,
            'Ubicación y horarios',
            'Visítanos en Santa Cruz',
            () => _go(context, const LocationScreen()),
          ),
          const SizedBox(height: 8),
          const Text(
            'Datos y precios demostrativos para fines académicos.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.black54, fontSize: 12),
          ),
        ],
      ),
    ),
  );
  void _go(BuildContext c, Widget w) =>
      Navigator.push(c, MaterialPageRoute(builder: (_) => w));
}

class _Banner extends StatelessWidget {
  const _Banner();
  @override
  Widget build(BuildContext c) => Container(
    padding: const EdgeInsets.all(24),
    decoration: BoxDecoration(
      borderRadius: BorderRadius.circular(24),
      gradient: const LinearGradient(colors: [coal, Color(0xFF563024), brand]),
    ),
    child: const Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Brasas del Oriente',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 27,
                  fontWeight: FontWeight.w800,
                ),
              ),
              SizedBox(height: 8),
              Text(
                'Parrilla, tradición y sabor cruceño.',
                style: TextStyle(color: Colors.white70, fontSize: 16),
              ),
            ],
          ),
        ),
        Icon(Icons.outdoor_grill, color: Color(0xFFF6B85C), size: 70),
      ],
    ),
  );
}

class _Access extends StatelessWidget {
  const _Access(this.icon, this.title, this.subtitle, this.tap);
  final IconData icon;
  final String title, subtitle;
  final VoidCallback tap;
  @override
  Widget build(BuildContext c) => Card(
    child: InkWell(
      onTap: tap,
      borderRadius: BorderRadius.circular(12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            CircleAvatar(
              backgroundColor: brand.withValues(alpha: .12),
              foregroundColor: brand,
              radius: 27,
              child: Icon(icon),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 17,
                    ),
                  ),
                  Text(subtitle, style: const TextStyle(color: Colors.black54)),
                ],
              ),
            ),
            const Icon(Icons.chevron_right),
          ],
        ),
      ),
    ),
  );
}

enum Category { todos, parrilladas, cortes, acompanamientos, bebidas }

extension CategoryName on Category {
  String get label => switch (this) {
    Category.todos => 'Todos',
    Category.parrilladas => 'Parrilladas',
    Category.cortes => 'Cortes',
    Category.acompanamientos => 'Acompañamientos',
    Category.bebidas => 'Bebidas',
  };
}

class Food {
  const Food(this.name, this.description, this.price, this.category, this.icon);
  final String name, description;
  final double price;
  final Category category;
  final IconData icon;
}

const menu = [
  Food(
    'Parrillada Oriente',
    'Carne, chorizo, pollo y guarniciones para compartir.',
    98,
    Category.parrilladas,
    Icons.outdoor_grill,
  ),
  Food(
    'Bife de chorizo',
    'Corte jugoso de res a la brasa, 350 g.',
    72,
    Category.cortes,
    Icons.restaurant,
  ),
  Food(
    'Lomo fino',
    'Medallón de res con salsa de la casa.',
    84,
    Category.cortes,
    Icons.local_fire_department,
  ),
  Food(
    'Yuca al horno',
    'Yuca dorada con mantequilla de hierbas.',
    15,
    Category.acompanamientos,
    Icons.bakery_dining,
  ),
  Food(
    'Ensalada criolla',
    'Tomate, cebolla y locoto fresco.',
    18,
    Category.acompanamientos,
    Icons.eco,
  ),
  Food(
    'Mocochinchi',
    'Bebida tradicional fría.',
    14,
    Category.bebidas,
    Icons.local_drink,
  ),
  Food(
    'Limonada de hierbabuena',
    'Refrescante y natural.',
    16,
    Category.bebidas,
    Icons.emoji_food_beverage,
  ),
];

class MenuScreen extends StatefulWidget {
  const MenuScreen({super.key});
  @override
  State<MenuScreen> createState() => _MenuState();
}

class _MenuState extends State<MenuScreen> {
  Category selected = Category.todos;
  @override
  Widget build(BuildContext c) {
    final items = selected == Category.todos
        ? menu
        : menu.where((x) => x.category == selected).toList();
    return Scaffold(
      appBar: AppBar(title: const Text('Menú digital')),
      body: Column(
        children: [
          const Padding(
            padding: EdgeInsets.all(12),
            child: Text('Precios demostrativos en bolivianos (Bs.)'),
          ),
          SizedBox(
            height: 46,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 12),
              children: Category.values
                  .map(
                    (x) => Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 4),
                      child: ChoiceChip(
                        label: Text(x.label),
                        selected: x == selected,
                        onSelected: (_) => setState(() => selected = x),
                      ),
                    ),
                  )
                  .toList(),
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: items.length,
              itemBuilder: (_, i) {
                final x = items[i];
                return Card(
                  child: ListTile(
                    contentPadding: const EdgeInsets.all(14),
                    leading: CircleAvatar(
                      backgroundColor: brand.withValues(alpha: .12),
                      foregroundColor: brand,
                      radius: 25,
                      child: Icon(x.icon),
                    ),
                    title: Text(
                      x.name,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(x.description),
                    trailing: Text(
                      'Bs. ${x.price.toStringAsFixed(0)}',
                      style: const TextStyle(
                        color: brand,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class ReservationScreen extends StatefulWidget {
  const ReservationScreen({super.key});
  @override
  State<ReservationScreen> createState() => _ReservationState();
}

class _ReservationState extends State<ReservationScreen> {
  final form = GlobalKey<FormState>(),
      name = TextEditingController(),
      people = TextEditingController(text: '2');
  DateTime? date;
  TimeOfDay? time;
  @override
  void dispose() {
    name.dispose();
    people.dispose();
    super.dispose();
  }

  Future<void> pickDate() async {
    final x = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 180)),
    );
    if (x != null) setState(() => date = x);
  }

  Future<void> pickTime() async {
    final x = await showTimePicker(
      context: context,
      initialTime: const TimeOfDay(hour: 20, minute: 0),
    );
    if (x != null) setState(() => time = x);
  }

  void confirm() {
    if (!form.currentState!.validate() || date == null || time == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Completa todos los datos de la reserva.'),
        ),
      );
      return;
    }
    showDialog<void>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Solicitud registrada'),
        content: Text(
          'Nombre: ${name.text}\nFecha: ${MaterialLocalizations.of(context).formatMediumDate(date!)}\nHora: ${time!.format(context)}\nPersonas: ${people.text}\n\nEsta es una simulación local; el restaurante deberá confirmar tu reserva.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cerrar'),
          ),
          FilledButton(
            onPressed: () => Navigator.popUntil(context, (r) => r.isFirst),
            child: const Text('Volver al inicio'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext c) => Scaffold(
    appBar: AppBar(title: const Text('Reservar mesa')),
    body: Form(
      key: form,
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Text(
            'Solicita tu mesa',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 6),
          const Text(
            'La confirmación final depende de la disponibilidad del restaurante.',
          ),
          const SizedBox(height: 22),
          TextFormField(
            controller: name,
            decoration: const InputDecoration(
              labelText: 'Nombre del cliente',
              prefixIcon: Icon(Icons.person),
            ),
            validator: (x) =>
                x == null || x.trim().isEmpty ? 'Ingresa tu nombre.' : null,
          ),
          const SizedBox(height: 14),
          OutlinedButton.icon(
            onPressed: pickDate,
            icon: const Icon(Icons.calendar_today),
            label: Text(
              date == null
                  ? 'Seleccionar fecha'
                  : MaterialLocalizations.of(c).formatMediumDate(date!),
            ),
          ),
          const SizedBox(height: 10),
          OutlinedButton.icon(
            onPressed: pickTime,
            icon: const Icon(Icons.access_time),
            label: Text(time == null ? 'Seleccionar hora' : time!.format(c)),
          ),
          const SizedBox(height: 14),
          TextFormField(
            controller: people,
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(
              labelText: 'Cantidad de personas',
              prefixIcon: Icon(Icons.groups),
            ),
            validator: (x) => int.tryParse(x ?? '') == null || int.parse(x!) < 1
                ? 'Ingresa una cantidad válida.'
                : null,
          ),
          const SizedBox(height: 24),
          FilledButton.icon(
            style: FilledButton.styleFrom(
              minimumSize: const Size.fromHeight(52),
              backgroundColor: brand,
            ),
            onPressed: confirm,
            icon: const Icon(Icons.check_circle),
            label: const Text('Confirmar reserva'),
          ),
        ],
      ),
    ),
  );
}

class LocationScreen extends StatelessWidget {
  const LocationScreen({super.key});
  static const address = 'Av. Ejemplo 123, Santa Cruz de la Sierra, Bolivia';
  Future<void> open(BuildContext c, String url) async {
    if (!await launchUrl(
          Uri.parse(url),
          mode: LaunchMode.externalApplication,
        ) &&
        c.mounted) {
      ScaffoldMessenger.of(c).showSnackBar(
        const SnackBar(
          content: Text('No se pudo abrir la aplicación externa.'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext c) => Scaffold(
    appBar: AppBar(title: const Text('Ubicación y horarios')),
    body: ListView(
      padding: const EdgeInsets.all(20),
      children: [
        const Icon(Icons.location_on, size: 62, color: brand),
        const SizedBox(height: 10),
        const Center(
          child: Text(
            'Brasas del Oriente',
            style: TextStyle(fontSize: 25, fontWeight: FontWeight.bold),
          ),
        ),
        const SizedBox(height: 24),
        const _Info(Icons.place, 'Dirección demostrativa', address),
        const _Info(
          Icons.schedule,
          'Horarios demostrativos',
          'Lunes a domingo\n12:00 a 15:30 y 18:30 a 23:00',
        ),
        const _Info(Icons.phone, 'Contacto demostrativo', '+591 70000000'),
        const SizedBox(height: 14),
        FilledButton.icon(
          style: FilledButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
            backgroundColor: brand,
          ),
          onPressed: () => open(
            c,
            'https://www.google.com/maps/search/?api=1&query=${Uri.encodeComponent(address)}',
          ),
          icon: const Icon(Icons.directions),
          label: const Text('Cómo llegar'),
        ),
        const SizedBox(height: 10),
        OutlinedButton.icon(
          style: OutlinedButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
          ),
          onPressed: () => open(
            c,
            'https://wa.me/59170000000?text=${Uri.encodeComponent('Hola, quisiera consultar sobre Brasas del Oriente.')}',
          ),
          icon: const Icon(Icons.chat),
          label: const Text('Contactar por WhatsApp'),
        ),
      ],
    ),
  );
}

class _Info extends StatelessWidget {
  const _Info(this.icon, this.title, this.text);
  final IconData icon;
  final String title, text;
  @override
  Widget build(BuildContext c) => Card(
    child: ListTile(
      leading: Icon(icon, color: brand),
      title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
      subtitle: Text(text),
    ),
  );
}
