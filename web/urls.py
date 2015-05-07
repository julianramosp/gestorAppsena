from django.conf.urls import patterns, url
from web import views
# Fecha creado: 25/08/2014
# Fecha actualizado: 05/09/2014
# Cambio realizado: Redefinir el metodo de carga de inventario, por la URL, Ln 9-13
urlpatterns = patterns('',
                        url(r'^$', views.index, name='index'),
                        url(r'^logout_view$', views.logout_view, name='logout'),
						url(r'^inventario/$', views.inventario, name='inventario'),
						url(r'^inventario/crear/compra$', views.CrearCompra, name='crearcompra'),
						url(r'^inventario/crear/detallecompra$', views.CrearDetalleCompra,name='creardetallecompra'),
						url(r'^inventario/cargar$',views.CargarInventario,name='cargarinventario'),
						url(r'^inventario/descargar$',views.DescargarInventario,name='descargarinventario'),
                        url(r'^venta/crearventaProducto$', views.crearventaProducto, name='venta'),
                        url(r'^ObtenerCliente$', views.ObtenerCliente, name='ObtenerCliente'),
                        url(r'^ObtenerProductos$', views.ObtenerProductos, name='ObtenerProductos'),
                        url(r'^ObtenerUVenta$', views.ObtenerUVenta, name='ObtenerUVenta'),
                        url(r'^ObtenerProductoPorReferencia$', views.ObtenerProductoPorReferencia, name='ObtenerProductoPorReferencia'),
                        url(r'^ObtenerInsumos$', views.ObtenerInsumos, name='ObtenerInsumos'),
                        url(r'^ObtenerUnidades$', views.ObtenerUnidades, name='ObtenerUnidades'),
                        url(r'^ObtenerUnidadesPorUVenta$', views.ObtenerUnidadesPorUVenta, name='ObtenerUnidadesPorUVenta'),
                        url(r'^ObtenerEquivalencia$', views.ObtenerEquivalencia, name='ObtenerEquivalencia'),
                        url(r'^venta/InsertarPreDetalleProducto$',views.InsertarPreDetalleProducto, name='InsertarPreDetalleProducto'),
                        url(r'^venta/ActualizarPreDetalleProducto$',views.ActualizarPreDetalleProducto, name='ActualizarPreDetalleProducto'),
                        url(r'^venta/EliminarPreDetalleProducto$',views.EliminarPreDetalleProducto, name='EliminarPreDetalleProducto'),
                        url(r'^venta/verFacturas$',views.verFacturas, name='verFacturas'),
                        url(r'^inventario/explosionMaterial$',views.crearExplosionMaterial, name='CrearExplosionMaterial'),
                        url(r'^inventario/ObtenerConsumosPorProductoTerminado$',views.ObtenerConsumosPorProductoTerminado, name='ObtenerConsumosPorProductoTerminado'),
                        url(r'^inventario/InsertarConsumo$',views.InsertarConsumo, name='InsertarConsumo'),
                        url(r'^inventario/ActualizarConsumo$',views.ActualizarConsumo, name='ActualizarConsumo'),
                        url(r'^inventario/EliminarConsumo$',views.EliminarConsumo, name='EliminarConsumo'),
                        url(r'^factura.pdf$', views.facturaPDF.as_view()),
                        url(r'^menu$',views.menu, name='Navegacion'),
                       )