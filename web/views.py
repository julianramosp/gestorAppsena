# Importacion de clases
# Fecha creado: 25/08/2014
# Fecha actualizado: 03/09/2014
# Cambio realizado: Importacion de forms
# Fecha actualizado: 05/09/2014
# Cambio realizado: Redefinicion del metodo CrearCompra() para inicio del cargue de inventario
# Fecha actualizado: 08/09/2014
# Cambio realizado: Carga de la clase Inventario procedente del modelo.
# Fecha actualizado: 12/09/2014
# Cambio realizado: Inclusion de la libreria de tiempo, Ln 15. Inclusion de la clase Producto desde el modelo, Ln 12
# Fecha actualizado: 17/09/2014
# Cambio realizado: Inclusion del modulo Compra_Material, Ln 14
# Fecha actualizado: 03/10/2014
# Cambio realizado: Inclusion de los modulos de facturacion, correspondiente a Empleado y Proveedor, Ln 17
from django.shortcuts import render, render_to_response
from web.models import Bodega, Inventario, Producto, Compra_Material, FormaPago, ResolucionFacturacion
from web.models import Proveedor, Empleado, Cliente, PreVenta, PreDetalleVenta, Unidad_de_Medida, Venta, DetalleVenta, ParametrosEmpresa, Empresa, Menu, Equivalencia_Unidad_Medidas, Consumo
from forms import BodegaForm, CrearCompraForm, CrearDetalleCompraForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from datetime import datetime
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django.core import serializers
from django.utils.timezone import get_current_timezone
import json
from easy_pdf.views import PDFTemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print user.has_perm('web.can_view_venta')
                print "ingreso satisfactorio"
                _empleado = Empleado.objects.get(User = user)
                request.session['empresa_id'] = _empleado.Empresa.Nit
                context = {}
                return render(request, 'web/base.html', context)
            else:
                context = {}
                return render(request, 'web/login.html', context)
        else:
            context = {}
            return render(request, 'web/login.html', context)
    else:
        if not request.user.is_authenticated():
            context = {}
            return render(request, 'web/login.html', context)
        else:
            context = {}
            return render(request, 'web/base.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/web/')

def menu(request):
    if request.GET["menu_id"]:
        _menu_id = request.GET["menu_id"]
        _menu = Menu.objects.get(id=_menu_id)
        _iconos = Menu.objects.filter(Habilitado=True,Tipo=1,Padre=_menu).order_by('Orden')

    context = {'menu':_menu,'iconos':_iconos}
    return render(request, 'web/menu.html', context)

def inventario(request):
	inventario = Inventario.objects.select_related('Producto')
	#qry	=	"SELECT * FROM web_inventario INNER JOIN web_producto ON ('web_producto.Ref_Producto'='web_inventario.Ref_Producto')"
	#inventario=Inventario.objects.raw(qry)
	return render(request,'web/inventario.html',{'inventario_lst':inventario})
	
# Vista para crear compra para surtir el inventario
# Fecha creado: 05/09/2014
# Fecha actualizado: 17/09/2014
# Cambio realizado: Devolver objeto a la vista, Ln 52. Almacenar el campo No_compra como string a la BD, Ln 41. FUENTE: http://bytes.com/topic/python/answers/20874-converting-integer-string
# Fecha actualizado: 02/10/2014 
# Cambio realizado: Almacenar los campos de las llaves foraneas correspondientes a proveedor y a empleado, Ln 56-58
# Fecha actualizado: 03/10/2014
# Cambio realizado: Cargue del proveedor, desde la variable id enviada por POST desde la vista crear_compra.html
def CrearCompra(request):
	if request.POST:
		form = CrearCompraForm(request.POST)
		if form.is_valid():
			#conversion a string
			num_compra = str(request.POST['No_compra'])
			#Carga de campos
			Fecha=request.POST['Fecha']
			Observaciones=request.POST['Observaciones']
			id=request.POST['id']
			Documento=request.POST['Documento']
			#Instancia de proveedor
			id=Proveedor.objects.get(id=id)
			#Instancia de empleado
			Documento=Empleado.objects.get(Documento=Documento)
			#Almacenamiento
			compra= Compra_Material(No_compra=num_compra,Fecha=Fecha,Observaciones=Observaciones,id=id,Documento=Documento)
			#form.save()
			compra.save()
			return HttpResponseRedirect('/web/inventario/crear/detallecompra')
	# Despliegue del formulario antes de enviar
	else:
		form = CrearCompraForm()
	args = {}
	args.update(csrf(request))
	
	args['form'] = form
	# Renderizar a la vista
	#return render_to_response('web/crear_compra.html', args)
	return render(request, 'web/crear_compra.html', args)
# Vista para crear detalle de compra
# Fecha creado: 05/09/2014
# Fecha actualizado: 11/09/2014
# Cambio realizado: Corregir redireccion, de tal manera que permita realizar pedido por varios materiales, Ln 57
# Observaciones: Para el metodo CargarInventario(), se le envia el proceso Entrante al inventario (ENT)
# Fecha actualizado: 17/09/2014
# Cambio realizado: Renderizar el template con el CSS del frontend, Ln 89
# Fecha actualizado: 22/09/2014
# Cambio realizado: Derivar los eventos, para causar el cierre de la Orden de compra (FUENTE: http://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form), Ln 79
def CrearDetalleCompra(request):
	if 'crearprod' in request.POST:
		form = CrearDetalleCompraForm(request.POST)
		if form.is_valid():
			form.save()
			# Gestion del inventario - Adicionar unidades a la entidad Gestion_Inventario
			#return HttpResponseRedirect('/web/inventario/')
			bod = request.POST['No_Posicion']
			prod = request.POST['Ref_Producto']
			estado = CargarInventario(request, 'ENT', bod, prod)
			return HttpResponseRedirect('detallecompra')
	elif 'cierreoc' in request.POST:
		CerrarOrden(request)
		inventario = Inventario.objects.select_related('Producto')	
		return render(request,'web/inventario.html',{'inventario_lst':inventario})
		
	# Despliegue del formulario antes de enviar
	else:
		form = CrearDetalleCompraForm()
	args={}
	args.update(csrf(request))
	args['form'] = form
	# Renderizar a la vista (template)

	#return render_to_response('web/crear_detalle_compra.html', args)
	return render(request, 'web/crear_detalle_compra.html', args)
# Metodo para implementar el cargue de inventario. Paso de la cantidad, el proceso (si es entrada o salida)

# Fecha creado: 08/09/2014
# Fecha actualizado: 11/09/2014
# Cambio realizado: Formular pseudocodigo para el proceso de inventario entrante, Ln 73-75
# Fecha actualizado: 12/09/2014
# Cambio realizado: Finalizar la rutina, para asignarla a la entidad de movimiento de inventario, Ln 80-81
def CargarInventario (request, proc, bod, prod):	
	cant = request.POST['Cantidad']
	if proc == 'ENT':
		# El inventario registra un entrante a la cantidad, al producto, y a la bodega
		bod=Bodega.objects.get(No_Posicion=bod)
		fhora= datetime.today()		
		prod=Producto.objects.get(Ref_Producto=prod)
		inv = Inventario(Cantidad=cant, Operacion=proc, Fecha_Hora=fhora, No_Posicion=bod, Ref_Producto=prod)
		inv.save()
		# Actualizo el inventario, sumando la cantidad pedida a la original
		ActualizarInventario(request, proc)
	#return true
	
# Vista para descargar elementos del inventario
# Fecha creado: 03/09/2014 

def DescargarInventario(request, proc, bod, prod):
	pass
# Proposito: Actualizar el inventario, sumando (o restando) la cantidad asociado al producto.
# Fecha creado: 22/09/2014
# Observaciones: 1.Acceso a queries mediante manual en la URL: https://docs.djangoproject.com/en/1.7/ref/models/queries/ 2.Conversion unicode a integer mediante la URL: http://bytes.com/topic/python/answers/164011-convert-unicode-int	
def ActualizarInventario(request, proc):
	#Cargar la cantidad actual
	Prod=Producto.objects.get(Ref_Producto=request.POST['Ref_Producto'])
	if proc == 'ENT':		
		#Actualizar la cantidad en la base
		Prod.Cantidad += int(request.POST['Cantidad'])
	elif proc == 'SAL':
		#Actualizar la cantidad en la base
		Prod.Cantidad -= int(request.POST['Cantidad'])
	#Actualizamos en la base
	Prod.save()

# Proposito: Cerrar la orden de compra, para no visualizarla al realizar la orden de pedido.
# Fecha creado: 22/09/2014
def CerrarOrden(request):
	ocompra=request.POST['No_compra']
	Compra=Compra_Material.objects.get(No_compra=ocompra)
	Compra.OC_cerrada=str(1)
	#Actualizamos en la base
	Compra.save()

def crearExplosionMaterial(request):
    if request.method=='POST' and 'cancel' in request.POST:
        return redirect('/web/')
    else:
        _productos = Producto.objects.filter(Tipo=0)
        context = {'productos_list':_productos}
        return render(request, 'web/explosion.html', context)

def crearventaProducto(request):
    if request.method=='POST' and 'create' in request.POST:
        _resolucionFactura = ResolucionFacturacion.objects.filter(Activo = True)[0]
        _base = _resolucionFactura.Base
        _numero = _resolucionFactura.Consecutivo_Inicial + _resolucionFactura.Secuencia
        _resolucionFactura.Secuencia = _resolucionFactura.Secuencia + 1
        _resolucionFactura.save()
        _numeroFactura = _base + str(_numero)
        _empleado = Empleado.objects.get(Documento=request.POST['selEmpleado'])
        _tz = get_current_timezone()
        #_fecha = _tz.localize(datetime.strptime(request.POST['txtFechaFactura'], '%d/%m/%Y'))
        _fecha = datetime.strptime(request.POST['txtFechaFactura'], '%d/%m/%Y')
        _cliente = Cliente.objects.get(Documento=request.POST['selCliente'])
        _observaciones = request.POST['txtObservaciones']
        _impuesto = request.POST['txtImpuesto']
        _total = request.POST['txtTotal']
        _formaPago = FormaPago.objects.get(id=request.POST['selFormaPago'])
        _factura = Venta.objects.create(Numero_Factura_Venta=_numeroFactura, Fecha=_fecha, Valor_Total_Compra=_total, Forma_Pago=_formaPago, Observaciones = _observaciones, Empleado = _empleado, Cliente = _cliente, Impuesto = _impuesto)
        _preventa = PreVenta.objects.get(id=request.POST['_id'])
        _preDetallesVenta = PreDetalleVenta.objects.filter(PreVenta=_preventa)
        for _predetalleVenta in _preDetallesVenta:
            _detalleVenta = DetalleVenta.objects.create(Descuento=_predetalleVenta.Descuento, Cantidad=_predetalleVenta.Cantidad, Observaciones=_predetalleVenta.Observaciones, Producto=_predetalleVenta.Producto, Numero_Factura=_factura, Valor_Unitario=_predetalleVenta.Valor_Unitario, SubTotal=_predetalleVenta.SubTotal)
            _predetalleVenta.delete()
        _preventa.delete()
        context = { 'factura': _factura,
                    'empresa': '899999034-1',
                  }
        return render(request, 'web/ventaPost.html', context)
    elif request.method=='POST' and 'preview' in request.POST:
        _empleado = Empleado.objects.get(Documento=request.POST['selEmpleado'])
        _tz = get_current_timezone()
        #_fecha = _tz.localize(datetime.strptime(request.POST['txtFechaFactura'], '%d/%m/%Y'))
        _fecha = datetime.strptime(request.POST['txtFechaFactura'], '%d/%m/%Y')
        _cliente = Cliente.objects.get(Documento=request.POST['selCliente'])
        _observaciones = request.POST['txtObservaciones']
        _impuesto = request.POST['txtImpuesto']
        _total = request.POST['txtTotal']
        _formaPago = FormaPago.objects.get(id=request.POST['selFormaPago'])
        _preventa = PreVenta.objects.get(id=request.POST['_id'])
        _preventa.Fecha = _fecha
        _preventa.Valor_Total_Compra = _total
        _preventa.Forma_Pago = _formaPago
        _preventa.Observaciones = _observaciones
        _preventa.Empleado = _empleado
        _preventa.Cliente = _cliente
        _preventa.Impuesto = _impuesto
        _preventa.save()
        return redirect('/web/')
    elif request.method=='POST' and 'cancel' in request.POST:
        _preventa = PreVenta.objects.get(id=request.POST['_id'])
        PreDetalleVenta.objects.filter(PreVenta=_preventa).delete()
        _preventa.delete()
        return redirect('/web/')
    else:
        empleados_list = Empleado.objects.all()
        clientes_list = Cliente.objects.all()
        forma_pago_list = FormaPago.objects.all()
        #pre_Venta = PreVenta.objects.create(Valor_Total_Compra=0)
        context = { 'empleados_list': empleados_list, 'clientes_list': clientes_list, 'forma_pago_list': forma_pago_list}
        return render(request, 'web/venta.html', context)

def verFacturas(request):
    context = {}
    return render(request, 'web/visorFacturas.html', context)

# PETICIONS JSON
def ObtenerCliente(request):
    _documento = request.GET['documento']
    _cliente = Cliente.objects.filter(Documento =_documento)
    data = serializers.serialize("json", _cliente)
    return HttpResponse(data, content_type='application/json')

def ObtenerProductos(request):
    _productos = Producto.objects.all()
    data = serializers.serialize("json", _productos)
    return HttpResponse(data, content_type='application/json')

def ObtenerProductoPorReferencia(request):
    _referencia = request.GET['referencia']
    _producto = Producto.objects.filter(Ref_Producto=_referencia)
    data = serializers.serialize("json", _producto)
    return HttpResponse(data, content_type='application/json')

def ObtenerUVenta(request):
    _uventa = Conversion_UndVenta_UndCompra.objects.all()
    data = serializers.serialize("json", _uventa)
    return HttpResponse(data, content_type='application/json')

def InsertarPreDetalleProducto(request):
    if request.GET['PreVenta'] == '0':
        _preventa = PreVenta.objects.create(Valor_Total_Compra=0)
    else:
        _preventa = PreVenta.objects.get(id=request.GET['PreVenta'])
    _descuento = request.GET['Descuento']
    _cantidad = request.GET['Cantidad']
    _observaciones = request.GET['Observaciones']
    _producto = Producto.objects.get(Ref_Producto=request.GET['Producto'])
    _valor_unitario = request.GET['Valor_Unitario']
    _subtotal = request.GET['SubTotal']
    _detalleVenta = PreDetalleVenta.objects.create(Descuento=_descuento, Cantidad=_cantidad, Observaciones=_observaciones, Producto=_producto, PreVenta=_preventa, Valor_Unitario=_valor_unitario, SubTotal=_subtotal)
    context = [{ 'preDetalleVenta': str(_detalleVenta), 'preVenta': str(_preventa), 'result': 'true'
    }]
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')

def ActualizarPreDetalleProducto(request):
    _id = request.GET['Id']
    _descuento = request.GET['Descuento']
    _cantidad = request.GET['Cantidad']
    _observaciones = request.GET['Observaciones']
    _producto = Producto.objects.get(Ref_Producto=request.GET['Producto'])
    _preventa = PreVenta.objects.get(id=request.GET['PreVenta'])
    _valor_unitario = request.GET['Valor_Unitario']
    _subtotal = request.GET['SubTotal']
    _detalleVenta = PreDetalleVenta.objects.get(id=_id)
    _detalleVenta.Descuento = _descuento
    _detalleVenta.Cantidad = _cantidad
    _detalleVenta.Observaciones = _observaciones
    _detalleVenta.Producto = _producto
    _detalleVenta.PreVenta  = _preventa
    _detalleVenta.Valor_Unitario = _valor_unitario
    _detalleVenta.SubTotal = _subtotal
    _detalleVenta.save()
    context = [{ 'preDetalleVenta': str(_detalleVenta), 'result': 'true'
    }]
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')

def EliminarPreDetalleProducto(request):
    _id = request.GET['Id']
    _detalleVenta = PreDetalleVenta.objects.get(id=_id)
    _detalleVenta.delete()
    context = [{ 'preDetalleVenta': str(_detalleVenta), 'result': 'true'
    }]
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')

def ObtenerProductoTerminado(request):
    _refProducto = request.GET['ref_producto']
    _productos = Producto.objects.filter(Ref_Producto=_refProducto)
    data = serializers.serialize("json", _productos)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def ObtenerInsumos(request):
    _productos = Producto.objects.filter(Tipo=1)
    data = serializers.serialize("json", _productos)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def ObtenerUnidades(request):
    _list = []
    _unidades = Unidad_de_Medida.objects.all()
    for unidad in _unidades:
        myDict = {}
        myDict["id"] = unidad.id
        myDict["name"] = unidad.Simbolo
        _list.append(myDict)
    data = json.dumps(_list)
    #data = serializers.serialize("json", _list)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def ObtenerUnidadesPorUVenta(request):
    _list = []
    _equivalentes = Equivalencia_Unidad_Medidas.objects.filter(Unidad_Venta=request.GET["uventa"])
    for _equivalente in _equivalentes:
        _unidad = Unidad_de_Medida.objects.get(id=_equivalente.Unidad_Compra.id)
        myDict = {}
        myDict["id"] = _unidad.id
        myDict["name"] = _unidad.Simbolo
        _list.append(myDict)
    data = json.dumps(_list)
    #data = serializers.serialize("json", _list)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def ObtenerEquivalencia(request):
    _uventa = request.GET["uventa"]
    _ucompra = request.GET["ucompra"]
    _equivalencia = Equivalencia_Unidad_Medidas.objects.filter(Unidad_Venta = _uventa, Unidad_Compra = _ucompra)[:1]
    #_list = []
    #myDict = {}
    #myDict["id"] = _equivalencia.id
    #myDict["equivalencia"] = _equivalencia.Equivalencia
    #_list.append(myDict)
    #data = json.dumps(_list)
    data = serializers.serialize("json", _equivalencia)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def ObtenerConsumosPorProductoTerminado(request):
    _Producto_Terminado_Id = request.GET["id"]
    _Consumos = Consumo.objects.filter(Producto_Terminado = _Producto_Terminado_Id)
    _list = []
    for _consumo in _Consumos:
        _Equivalencia_Unidad_Medidas = Equivalencia_Unidad_Medidas.objects.filter(Unidad_Venta=_consumo.Insumo.Unidad_Venta.id, Unidad_Compra=_consumo.Unidad_Consumo.id)[:1]
        myDict = {}
        myDict["id"] = _consumo.id
        myDict["Ref_Producto"] = _consumo.Insumo.Ref_Producto
        myDict["Nombre_producto"] = _consumo.Insumo.Nombre_producto
        myDict["Unidad_Venta"] = _consumo.Insumo.Unidad_Venta.id
        myDict["Unidad_Consumo"] = _consumo.Unidad_Consumo.id
        myDict["Equivalencia"] = str(_Equivalencia_Unidad_Medidas[0].Equivalencia)
        myDict["V_Unitario"] = str(_consumo.Insumo.Valor_Unitario)
        myDict["Consumo"] = str(_consumo.Consumo)
        myDict["Desperdicio"] = str(_consumo.Desperdicio)
        myDict["ConsumoReal"] = str(_consumo.Consumo_Real)
        myDict["PrecioConsumo"] = str(_consumo.Precio_Consumo)
        _list.append(myDict)
    data = json.dumps(_list)
    return HttpResponse(data, content_type='application/json')

def InsertarConsumo(request):
    _Producto_Terminado = Producto.objects.get(Ref_Producto=request.GET["Producto_Terminado"])
    _Insumo = Producto.objects.get(Ref_Producto=request.GET["Insumo"])
    _Unidad_Consumo = Unidad_de_Medida.objects.get(id=request.GET["Unidad_Consumo"])
    _Consumo = request.GET["Consumo"]
    _Desperdicio = request.GET["Desperdicio"]
    _Consumo_Real = request.GET["Consumo_Real"]
    _Precio_Consumo = request.GET["Precio_Consumo"]
    _ConsumoRow = Consumo.objects.create(Producto_Terminado = _Producto_Terminado, Insumo = _Insumo, Unidad_Consumo = _Unidad_Consumo, Consumo = _Consumo, Desperdicio = _Desperdicio, Consumo_Real = _Consumo_Real, Precio_Consumo = _Precio_Consumo)
    context = [{ 'ConsumoRow': str(_ConsumoRow), 'result': 'true'}]
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')

def ActualizarConsumo(request):
    _id = request.GET['id']
    _Producto_Terminado = Producto.objects.get(Ref_Producto=request.GET["Producto_Terminado"])
    _Insumo = Producto.objects.get(Ref_Producto=request.GET["Insumo"])
    _Unidad_Consumo = Unidad_de_Medida.objects.get(id=request.GET["Unidad_Consumo"])
    _Consumo = request.GET["Consumo"]
    _Desperdicio = request.GET["Desperdicio"]
    _Consumo_Real = request.GET["Consumo_Real"]
    _Precio_Consumo = request.GET["Precio_Consumo"]
    _ConsumoRow = Consumo.objects.get(id=_id)
    _ConsumoRow.Producto_Terminado = _Producto_Terminado
    _ConsumoRow.Insumo = _Insumo
    _ConsumoRow.Unidad_Consumo = _Unidad_Consumo
    _ConsumoRow.Consumo = _Consumo
    _ConsumoRow.Desperdicio = _Desperdicio
    _ConsumoRow.Consumo_Real = _Consumo_Real
    _ConsumoRow.Precio_Consumo = _Precio_Consumo
    _ConsumoRow.save()
    context = [{ 'ConsumoRow': str(_ConsumoRow), 'result': 'true'}]
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')

def EliminarConsumo(request):
    _id = request.GET['id']
    _ConsumoRow = Consumo.objects.get(id=_id)
    _ConsumoRow.delete()
    context = [{ 'ConsumoRow': str(_ConsumoRow), 'result': 'true'}]
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')


#PDF
class facturaPDF(PDFTemplateView):
    template_name = "facturaTemplate.html"

    def get_context_data(self, **kwargs):
        _venta = Venta.objects.get(Numero_Factura_Venta=self.request.GET['id'])
        _detalleVenta = DetalleVenta.objects.filter(Numero_Factura = _venta)
        _empresaGet = self.request.session['empresa_id']
        _parametrosEmpresa = ParametrosEmpresa.objects.get(Empresa = _empresaGet)
        _empresa = Empresa.objects.get(Nit=_empresaGet)
        _subtotal = _venta.Valor_Total_Compra - _venta.Impuesto
        return super(facturaPDF, self).get_context_data(
            pagesize="Letter",
            venta=_venta,
            detalleVenta = _detalleVenta,
            parametrosEmpresa = _parametrosEmpresa,
            empresa = _empresa,
            subtotal = _subtotal,
            **kwargs
        )