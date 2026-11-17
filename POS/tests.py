import json
from unittest.mock import MagicMock, patch
from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from POS import services


@override_settings(SESSION_ENGINE='django.contrib.sessions.backends.cache')
class SecurityViewsTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    def _login_session(self, es_admin='N', es_supervisor='N'):
        session = self.client.session
        session['usuario_activo'] = {
            'id': 10,
            'nombre': 'GARZON PRUEBA',
            'es_admin': es_admin,
            'es_supervisor': es_supervisor,
        }
        session['nombre_local'] = 'Merquen Test'
        session.save()

    @patch('MerquenPOS.views.services.obtener_nombre_local', return_value='Merquen Test')
    @patch('MerquenPOS.views.services.obtener_usuarios_activos', return_value=[{'nombre': 'ADMIN'}])
    @patch('MerquenPOS.views.services.verificar_login', return_value=None)
    def test_login_rate_limiting_blocks_after_max_attempts(self, mock_verificar, mock_usuarios, mock_local):
        url = reverse('login')
        for _ in range(5):
            response = self.client.post(url, {'usuario': 'ADMIN', 'password': 'bad'})
            self.assertEqual(response.status_code, 200)

        self.assertEqual(mock_verificar.call_count, 5)

        # El sexto intento debe bloquearse sin consultar verificar_login nuevamente
        response = self.client.post(url, {'usuario': 'ADMIN', 'password': 'bad'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Demasiados intentos fallidos')
        self.assertEqual(mock_verificar.call_count, 5)

    def test_admin_route_is_disabled(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 404)

    @patch('POS.views.services.anular_cuenta')
    def test_api_anular_ticket_denies_non_privileged_user_with_consumos(self, mock_anular):
        self._login_session(es_admin='N', es_supervisor='N')
        mock_anular.side_effect = ValueError("No se puede anular una cuenta que tiene productos registrados.")

        response = self.client.post(
            reverse('api_anular_ticket'),
            data=json.dumps({'folio': '1001'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)
        mock_anular.assert_called_once_with('1001', permitir_con_consumos=False)

    @patch('POS.views.services.anular_cuenta')
    def test_api_anular_ticket_allows_supervisor(self, mock_anular):
        self._login_session(es_admin='N', es_supervisor='S')

        response = self.client.post(
            reverse('api_anular_ticket'),
            data=json.dumps({'folio': '1001'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        mock_anular.assert_called_once_with('1001', permitir_con_consumos=True)

    @patch('POS.views.services.agregar_producto_consumo')
    def test_api_agregar_ticket_hides_internal_database_errors(self, mock_agregar):
        self._login_session()
        mock_agregar.side_effect = RuntimeError("ODBC SQL Server Driver internal table detail XY123")

        response = self.client.post(
            reverse('api_agregar_ticket'),
            data=json.dumps({
                'folio': '1001',
                'punto': '01',
                'cuenta': '1',
                'producto_padre': {
                    'producto': 'P01',
                    'clase': 'C1',
                    'grupo': 'G1',
                    'precio': 5000,
                    'cantidad': 1,
                }
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 500)
        payload = response.json()
        self.assertEqual(payload['status'], 'error')
        self.assertNotIn('XY123', payload['message'])
        self.assertNotIn('ODBC', payload['message'])


class SecurityServicesTests(SimpleTestCase):
    def test_cubiertos_validation_rejects_invalid_values(self):
        with self.assertRaises(ValueError):
            services.crear_nueva_cuenta.__wrapped__('01', '5', 1, 0)
        with self.assertRaises(ValueError):
            services.crear_nueva_cuenta.__wrapped__('01', '5', 1, -3)
        with self.assertRaises(ValueError):
            services.crear_nueva_cuenta.__wrapped__('01', '5', 1, 1000)
        with self.assertRaises(ValueError):
            services.actualizar_cubiertos_cuenta('1001', 'abc')

    @patch('POS.services.verificar_tiene_consumos', return_value=True)
    @patch('POS.services.connection')
    def test_anular_cuenta_blocks_when_consumos_exist_and_not_authorized(self, mock_conn, mock_tiene):
        with self.assertRaises(ValueError):
            services.anular_cuenta('1001', permitir_con_consumos=False)
        mock_conn.cursor.assert_not_called()

    @patch('POS.services.obtener_turno_activo', return_value={'fecha': '17/11/2026', 'turno_bd': '1'})
    @patch('POS.services.obtener_precio_producto', return_value=9500.0)
    @patch('POS.services.connection')
    def test_agregar_producto_consumo_uses_server_price_and_rejects_negative_qty(
        self, mock_conn, mock_precio, mock_turno
    ):
        # 1. Cantidad negativa o cero debe fallar antes de tocar la BD
        with self.assertRaises(ValueError):
            services.agregar_producto_consumo.__wrapped__(
                folio='1001',
                punto='01',
                cuenta='1',
                usuario_id=10,
                producto_padre={'clase': 'C1', 'grupo': 'G1', 'producto': 'P1', 'cantidad': -1, 'precio': 10},
                opciones=[],
            )

        # 2. Precio manipulado por el cliente (precio=1) debe ser ignorado y usar 9500.0 del servidor
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        # fetchone side effects: [None (no agrupable), ('5',) (mesa), (101,) (subindice insertado)]
        mock_cursor.fetchone.side_effect = [None, ('5',), (101,)]

        services.agregar_producto_consumo.__wrapped__(
            folio='1001',
            punto='01',
            cuenta='1',
            usuario_id=10,
            producto_padre={'clase': 'C1', 'grupo': 'G1', 'producto': 'P1', 'cantidad': 2, 'precio': 1},
            opciones=[],
        )

        mock_precio.assert_called_once_with('01', 'C1', 'G1', 'P1')
        # Verificar que el INSERT usó el precio del servidor (9500.0) y no 1
        insert_call_args = mock_cursor.execute.call_args_list[2][0][1]
        self.assertIn(9500.0, insert_call_args)
        self.assertNotIn(1, [x for x in insert_call_args if isinstance(x, float)])


@override_settings(SESSION_ENGINE='django.contrib.sessions.backends.cache')
class TemplateContrastTests(SimpleTestCase):
    def _login_session(self):
        session = self.client.session
        session['usuario_activo'] = {
            'id': 10,
            'nombre': 'GARZON PRUEBA',
            'es_admin': 'N',
            'es_supervisor': 'N',
        }
        session['nombre_local'] = 'Merquen Test'
        session.save()

    @patch('MerquenPOS.views.services.obtener_nombre_local', return_value='Merquen Test')
    @patch('MerquenPOS.views.services.obtener_usuarios_activos', return_value=[{'nombre': 'ADMIN'}])
    def test_login_template_uses_modern_tokens(self, mock_usuarios, mock_local):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '--color-boton: #10b981;')
        self.assertContains(response, '--color-fondo: #f1f5f9;')

    @patch('POS.views.services.obtener_turno_activo', return_value={'fecha': '17/11/2026', 'turno_texto': 'DIA'})
    @patch('POS.views.services.getEstadoMesas', return_value=[
        {'numero': '1', 'estado': 'libre', 'bloqueada': False, 'usuarioBloqueo': ''}
    ])
    @patch('POS.views.services.getPuntosVenta', return_value=[{'codigo': '01', 'nombre': 'SALON'}])
    def test_mesas_template_uses_modern_palette_and_subtle_libre(self, mock_puntos, mock_mesas, mock_turno):
        self._login_session()
        response = self.client.get(reverse('seleccion_mesas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '--border-libre: #cbd5e1;')
        self.assertContains(response, '--border-ocupada: #93c5fd;')
        self.assertContains(response, '--border-impresa: #fca5a5;')
        self.assertContains(response, 'opacity: 0.7;')

    @patch('POS.views.services.obtener_consumos_mesa', return_value=[])
    @patch('POS.views.services.obtener_detalles_cuenta', return_value={
        'cubiertos': 2,
        'nombre_garzon': 'GARZON PRUEBA',
        'cuentas_activas': ['1'],
    })
    @patch('POS.views.services.get_punto_nombre', return_value='SALON PRINCIPAL')
    @patch('POS.views.services.get_familias_punto', return_value=[{'clase': '01', 'nombre': 'COCINA'}])
    @patch('POS.views.services.obtener_turno_activo', return_value={'fecha': '17/11/2026', 'turno_texto': 'DIA'})
    def test_comanda_template_uses_modern_group_and_readable_note_styles(
        self, mock_turno, mock_fam, mock_npunto, mock_det, mock_cons
    ):
        self._login_session()
        response = self.client.get(reverse('comanda', args=['01', '1', '1001']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '--color-grupo: #0ea5e9;')
        self.assertContains(response, '.nota-ticket')
        self.assertNotContains(response, "noteElement.className = 'text-warning")

