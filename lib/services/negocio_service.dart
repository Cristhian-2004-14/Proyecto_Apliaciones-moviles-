import 'package:supabase_flutter/supabase_flutter.dart';

import '../config/supabase_config.dart';
import '../data/negocios_demo.dart';
import '../models/negocio.dart';

class NegocioService {
  Future<List<Negocio>> obtenerNegocios() async {
    if (!SupabaseConfig.isConfigured) return negociosDemo;

    final rows = await Supabase.instance.client
        .from('negocios')
        .select()
        .order('id');
    return (rows as List)
        .cast<Map<String, dynamic>>()
        .map(Negocio.fromMap)
        .toList();
  }
}
