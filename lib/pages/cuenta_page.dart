import 'package:flutter/material.dart';

import '../config/supabase_config.dart';
import '../core/validators.dart';
import '../models/perfil.dart';
import '../services/auth_service.dart';
import 'foto_negocio_page.dart';
import 'fotos_productos_page.dart';
import 'configuracion_qr_page.dart';
import 'panel_pedidos_page.dart';
import 'verificacion_pagos_page.dart';

class CuentaPage extends StatefulWidget {
  const CuentaPage({super.key});

  @override
  State<CuentaPage> createState() => _CuentaPageState();
}

class _CuentaPageState extends State<CuentaPage> {
  final _service = AuthService();
  final _formKey = GlobalKey<FormState>();
  final _nombre = TextEditingController();
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _registro = false;
  bool _enviando = false;
  late Future<Perfil?> _perfilFuture;

  @override
  void initState() {
    super.initState();
    _perfilFuture = SupabaseConfig.isConfigured
        ? _service.obtenerPerfil()
        : Future.value(null);
  }

  @override
  void dispose() {
    _nombre.dispose();
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  void _reload() {
    setState(() {
      _perfilFuture = SupabaseConfig.isConfigured
          ? _service.obtenerPerfil()
          : Future.value(null);
    });
  }

  Future<void> _enviar() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _enviando = true);
    try {
      if (_registro) {
        await _service.registrar(
          nombre: _nombre.text,
          email: _email.text,
          password: _password.text,
        );
      } else {
        await _service.iniciarSesion(
          email: _email.text,
          password: _password.text,
        );
      }
      if (!mounted) return;
      _reload();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            _registro
                ? 'Cuenta creada. Revisa tu correo si se requiere confirmación.'
                : 'Sesión iniciada correctamente.',
          ),
        ),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('No se pudo completar la operación: $error')),
      );
    } finally {
      if (mounted) setState(() => _enviando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!SupabaseConfig.isConfigured) {
      return const Scaffold(
        body: Center(child: Text('Configura Supabase para usar cuentas.')),
      );
    }
    if (_service.usuarioActual == null) return _buildAcceso(context);
    return _buildPerfil(context);
  }

  Widget _buildAcceso(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Mi cuenta')),
    body: Form(
      key: _formKey,
      child: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text(
            _registro ? 'Crear cuenta' : 'Iniciar sesión',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 16),
          if (_registro) ...[
            TextFormField(
              controller: _nombre,
              decoration: const InputDecoration(labelText: 'Nombre'),
              validator: Validators.requiredName,
            ),
            const SizedBox(height: 12),
          ],
          TextFormField(
            controller: _email,
            keyboardType: TextInputType.emailAddress,
            decoration: const InputDecoration(labelText: 'Correo electrónico'),
            validator: (value) => (value ?? '').contains('@')
                ? null
                : 'Ingresa un correo válido.',
          ),
          const SizedBox(height: 12),
          TextFormField(
            controller: _password,
            obscureText: true,
            decoration: const InputDecoration(labelText: 'Contraseña'),
            validator: (value) =>
                (value ?? '').length >= 6 ? null : 'Mínimo 6 caracteres.',
          ),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: _enviando ? null : _enviar,
            child: Text(_registro ? 'Crear cuenta' : 'Ingresar'),
          ),
          TextButton(
            onPressed: _enviando
                ? null
                : () => setState(() => _registro = !_registro),
            child: Text(_registro ? 'Ya tengo una cuenta' : 'Crear una cuenta'),
          ),
        ],
      ),
    ),
  );

  Widget _buildPerfil(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Mi cuenta')),
    body: FutureBuilder<Perfil?>(
      future: _perfilFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasError || snapshot.data == null) {
          return Center(
            child: FilledButton(
              onPressed: _reload,
              child: const Text('Reintentar'),
            ),
          );
        }
        final perfil = snapshot.data!;
        return ListView(
          padding: const EdgeInsets.all(20),
          children: [
            const Icon(Icons.account_circle, size: 78),
            const SizedBox(height: 12),
            Center(
              child: Text(
                perfil.nombre,
                style: Theme.of(context).textTheme.headlineSmall,
              ),
            ),
            const SizedBox(height: 8),
            Center(child: Text('Rol: ${perfil.esDueno ? 'Dueño' : 'Cliente'}')),
            const SizedBox(height: 24),
            if (perfil.esDueno)
              FilledButton.icon(
                onPressed: () => Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const PanelPedidosPage()),
                ),
                icon: const Icon(Icons.admin_panel_settings_outlined),
                label: const Text('Abrir panel del dueño'),
              ),
            if (perfil.esDueno) ...[
              const SizedBox(height: 10),
              OutlinedButton.icon(
                onPressed: () => Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const FotoNegocioPage()),
                ),
                icon: const Icon(Icons.photo_camera_back_outlined),
                label: const Text('Cambiar foto de portada'),
              ),
              const SizedBox(height: 10),
              OutlinedButton.icon(
                onPressed: () => Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const FotosProductosPage()),
                ),
                icon: const Icon(Icons.photo_library_outlined),
                label: const Text('Gestionar fotos de productos'),
              ),
              const SizedBox(height: 10),
              OutlinedButton.icon(
                onPressed: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const ConfiguracionQrPage(),
                  ),
                ),
                icon: const Icon(Icons.qr_code_2_outlined),
                label: const Text('Configurar QR de pagos'),
              ),
              const SizedBox(height: 10),
              FilledButton.icon(
                onPressed: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const VerificacionPagosPage(),
                  ),
                ),
                icon: const Icon(Icons.verified_user_outlined),
                label: const Text('Verificación de pagos'),
              ),
            ],
            const SizedBox(height: 10),
            OutlinedButton.icon(
              onPressed: () async {
                await _service.cerrarSesion();
                _reload();
              },
              icon: const Icon(Icons.logout),
              label: const Text('Cerrar sesión'),
            ),
          ],
        );
      },
    ),
  );
}
