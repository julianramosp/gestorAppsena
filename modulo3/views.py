# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from modulo3.models import Tipo_De_Dia, Franja_Jornada, Jornada_Laboral, Dia_Laboral,Generalidad_Tiempos, Suplemento_Fisico, Suplemento_Mental, Suplemento_Monotonia
from modulo3.models import Suplemento_Ambiental, Suplemento_Genero,Calificacion_Habilidad,Calificacion_Consistencia,Calificacion_Esfuerzo
from modulo3.models import Producto_Referencia,Tiempos_Por_Actividad, Maquina,Ruta_Operacional
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from datetime import datetime
from django.core.context_processors import csrf
from django.shortcuts import redirect
from django.core import serializers
from django.utils.timezone import get_current_timezone
import json
from decimal import *
from django.views.decorators.csrf import csrf_exempt
from geraldo.generators import PDFGenerator
from django.http import Http404
from django.shortcuts import render_to_response
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string




#funcion para cambiar formato a decimal

def cambio_formato(valor):
            _a_decimal = valor.replace(",",".")
            _resultado_dec= Decimal(_a_decimal)
            return _resultado_dec

# Create your views here.
def index(request):
    context = {}
    return render(request, 'web/base.html', context)

def JornadaLaboral(request):
    if request.method=='POST':
		#leemos elementos
        _sumajornada= request.POST['sumajornada']
        _tipojornada = Tipo_De_Dia.objects.get(id=request.POST['selTipoDia'])
        _idDias= request.POST['idtotaljornada']#hidden para traer el id
		#cargamos objeto
        _cargadia = Dia_Laboral.objects.get(id=_idDias)
        _cargadia.Total = _sumajornada
        _cargadia.Tipo_De_Dia = _tipojornada
        _cargadia.save()
        tipoDiaList = Tipo_De_Dia.objects.all()
        context = {'tipodia_list': tipoDiaList}
        return HttpResponseRedirect('/modulo3/GeneralidadTiempos')
        #return render(request, 'web/jornadaLaboral.html', context)
    else:
		tipoDiaList = Tipo_De_Dia.objects.all()
		context = {'tipodia_list': tipoDiaList}
		return render(request, 'web/jornadaLaboral.html', context)
	
	
def GeneralidadTiempos(request):
    if request.method=='POST' :
        _actividad = request.POST['Actividad']
        _total_promedio = request.POST['promedio']
        _repeticiones = request.POST['repeticiones']
        _tiempoestandard = request.POST['estandard']
        _suplementofisico =Suplemento_Fisico.objects.filter(S_Fisico = cambio_formato(request.POST['supFisico']))[0]
        _suplementoMental = Suplemento_Mental.objects.filter(S_Mental = cambio_formato(request.POST['supMental']))[0]
        _suplementomonotonia =request.POST['monotonia']
        _suplementoGenero =  Suplemento_Genero.objects.filter(S_Genero = cambio_formato(request.POST['supGenero']))[0]
        _suplemento_Ambiental = Suplemento_Ambiental.objects.filter(S_Ambiental= cambio_formato(request.POST['supAmbiental']))[0] 
        _cal_habilidad = Calificacion_Habilidad.objects.filter(C_Habilidad = cambio_formato(request.POST['calHabilidad']))[0]
        _cal_consistencia = Calificacion_Consistencia.objects.filter(C_Consistencia = cambio_formato(request.POST['calConsistencia']))[0]
        _cal_esfuerzo = Calificacion_Esfuerzo.objects.filter(C_Esfuerzo= cambio_formato(request.POST['calEsfuerzo']))[0]
		#cargar objetos
        _toma_tiempos = Generalidad_Tiempos.objects.get(id =request.POST['calculodetiempos'])
        _toma_tiempos.Actividad = _actividad
        _toma_tiempos.Numero_Repeticiones=_repeticiones
        _toma_tiempos.Tiempo_Promedio =_total_promedio
        _toma_tiempos.Tiempo_Estandard =_tiempoestandard
        _toma_tiempos.S_Fisico=_suplementofisico
        _toma_tiempos.S_Mental = _suplementoMental
        _toma_tiempos.Suplemento_Genero = _suplementoGenero
        _toma_tiempos.S_Ambiental = _suplemento_Ambiental
        _toma_tiempos.Sup_Monotonia=_suplementomonotonia
        _toma_tiempos.Calificacion_Habilidad=_cal_habilidad 
        _toma_tiempos.Calificacion_Consistencia=_cal_consistencia
        _toma_tiempos.Calificacion_Esfuerzo=_cal_esfuerzo
        _toma_tiempos.save()
        tomaDetiempos = Generalidad_Tiempos.objects.all()
        context={'toma_tiempos':tomaDetiempos}
        return HttpResponseRedirect('/modulo3/BalanceoDeProduccion')
    else:    
        tomaDetiempos = Generalidad_Tiempos.objects.all()
        suplemento_fisico = Suplemento_Fisico.objects.all()
        suplemento_mental = Suplemento_Mental.objects.all()
        suplemento_ambiental=Suplemento_Ambiental.objects.all()
        suplemento_genero = Suplemento_Genero.objects.all()
        calificacion_habilidad= Calificacion_Habilidad.objects.all()
        calificacion_consistencia= Calificacion_Consistencia.objects.all()
        calificacion_esfuerzo= Calificacion_Esfuerzo.objects.all()
        context ={'toma_tiempos':tomaDetiempos, 'suplementofisico':suplemento_fisico,'suplementomental':suplemento_mental,
        'suplementoambiental':suplemento_ambiental, 'suplementogenero':suplemento_genero,
        'calificacionhabilidad':calificacion_habilidad,'calificacionconsistencia':calificacion_consistencia,'calificacionesfuerzo':calificacion_esfuerzo
        }
        return render(request,'web/GeneralidadTiempos.html',context)
	
def BalanceoDeProduccion(request):
    if request.method=='POST':
        producto = request.POST['Producto']
        tipo_de_dia = Dia_Laboral.objects.get(id=request.POST['selTipoDia'])
        total_jornada = request.POST['Tiempo_total']
        eficiencia_modulo = request.POST['eficiencia']
        lote = request.POST['lote']
        estandard_total = request.POST['estandard']
        total_RH = request.POST['total_RH']
        total_lote = request.POST['total_lote']	
        idbalanceo= request.POST['idbalanceo']#hidden para traer el id ??? COMO TRAEMOS EL ID
        #Carga de objetos
        total_balanceo  = Producto_Referencia.objects.get(id =request.POST['idbalanceo'])
        total_balanceo.Nombre_Producto =producto
        total_balanceo.Tipo_De_Dia = tipo_de_dia
        total_balanceo.Total_jornada = total_jornada
        total_balanceo.Eficiencia = eficiencia_modulo
        total_balanceo.Lote_A_Fabricar = lote
        total_balanceo.Suma_Tiempo_Estandard = estandard_total
        total_balanceo.Tiempo_Total_lote = total_lote
        total_balanceo.Total_Recurso_humano =  total_RH
        total_balanceo.Total_Recurso_por_actividad=total_lote
        parametro = total_balanceo.id
        total_balanceo.save()
        if 'guardar' in request.POST:
          return HttpResponseRedirect('/modulo3/BalanceoDeProduccion')
        elif 'reportes' in request.POST:  
          return HttpResponseRedirect('/reports/')
        else:
          return HttpResponseRedirect('/modulo3/modulo3_reporte/%s/'%parametro)

    else:
        _nombre_producto = Producto_Referencia.objects.all()
        _tipo_de_dia_guardado= Dia_Laboral.objects.all()
        _actividad_guardada =Generalidad_Tiempos.objects.all()
        _recurso = Maquina.objects.all()
        context = {'nombreproducto':_nombre_producto,'tipodia_list':_tipo_de_dia_guardado,'actividadguardada':_actividad_guardada,'recurso':_recurso }
        return render(request, 'web/BalanceoDeProduccion.html', context)
 	
	

#peticiones JSON
#base de datos Franja jornada
def TiemposPorFranja(request):
    _tiempos = Franja_Jornada.objects.all() #creo variable y llamo a la tabla cargue combo box parte de
    data = serializers.serialize("json",_tiempos)
	#retorna le informacion en formato json
    return HttpResponse(data, content_type = 'aplication/json')



#funcion para insertar resultado y lo guardado 
def Insert_Sum_Tiempos(request):
	_tipoDeDia = request.GET['Tipo_De_Dia']
	_franja = Franja_Jornada.objects.get(id=request.GET['Franja_De_Tiempo'])
	_t_inicio = request.GET['Tiempo_Inicio']
	_t_fin = request.GET['Tiempo_Fin']
	_subtotal = request.GET['Subtotal']
	if _tipoDeDia == "0":
		_diaLaboral = Dia_Laboral.objects.create()
	else:
		_diaLaboral = Dia_Laboral.objects.get(id=_tipoDeDia)
	_TotalTiempoJornada = Jornada_Laboral.objects.create( Tipo_De_Dia = _diaLaboral,Franja_De_Tiempo =_franja, Tiempo_Inicio=_t_inicio , Tiempo_Fin=_t_fin, SubTotal=_subtotal)
	context = [{'JornadaLaboral_id':str(_TotalTiempoJornada), 'diaLaboral_id':_diaLaboral.id,'result':'true'}]
	data = json.dumps(context)
	return HttpResponse(data, content_type='application/json')
	
	
def Actualizar_Tiempos(request):
	_id = request.GET['id']
	_franja = Franja_Jornada.objects.get(id=request.GET['Franja_De_Tiempo'])
	_t_inicio = request.GET['Tiempo_Inicio']
	_t_fin = request.GET['Tiempo_Fin']
	_subtotal = request.GET['Subtotal']
	_TotalTiemposJornada = Jornada_Laboral.objects.get(id=_id)
	_TotalTiemposJornada.Franja_De_Tiempo = _franja
	_TotalTiemposJornada.Tiempo_Inicio = _t_inicio 
	_TotalTiemposJornada.Tiempo_Fin =  _t_fin 
	_TotalTiemposJornada.SubTotal = _subtotal
	_TotalTiemposJornada.save()
	context = [{ 'sumatoriaJornada': str(_TotalTiemposJornada), 'result': 'true'}]
	data = json.dumps(context)
	return HttpResponse(data, content_type='application/json')

def EliminarRegistroDeTiempo(request):
   _id = request.GET['Id']
   _TotalTiemposJornada = Jornada_Laboral.objects.get(id=_id)
   _TotalTiemposJornada.delete()
   context = [{ 'eliminarRegistro': str(_TotalTiemposJornada), 'result': 'true'
   }]
   data = json.dumps(context)
   return HttpResponse(data, content_type='application/json')	

   #plantilla 3 peticion json
   
def TomadeTiempos(request):
  _tiempo_muestra= request.GET['Tiempos_Por_Actividad']
  if request.GET['Actividad'] == "0":
        _nuevaactividad = Generalidad_Tiempos.objects.create()
  else:
        _nuevaactividad = Generalidad_Tiempos.objects.get(id=request.GET['Actividad'])
  _totalToma = Tiempos_Por_Actividad.objects.create(Actividad  =_nuevaactividad,Muestras_Tiempo = _tiempo_muestra)
  context = [{'Tiempo_Muestra_id':str(_totalToma),'nuevaactividad_id':str(_nuevaactividad.id), 'result':'true'
  
  }]
  data = json.dumps(context)
  return HttpResponse(data, content_type='application/json')
	
	
def EditarTomadeTiempos (request):
     _id = request.GET['Id']
     _tiempo_muestra= request.GET['Tiempos_Por_Actividad']
     _totalToma = Tiempos_Por_Actividad.objects.get(id=_id)
     _totalToma.Muestras_Tiempo = _tiempo_muestra
     _totalToma.save()
     context = [{ 'actualizartiempos': str(_totalToma), 'result': 'true'}]
     data = json.dumps(context)
     return HttpResponse(data, content_type='application/json')
	
def EliminarTomadeTiempos(request):
    _id = request.GET['id']
    _totalToma = Tiempos_Por_Actividad.objects.get(id=_id)
    _totalToma.delete()
    context = [{ 'EliminarTomadeTiempos': str(_totalToma), 'result': 'true'
    }]
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')	
#creación de url para traer campos de generalidad de tiempos(actividad y tiempo estandard)	
@csrf_exempt
def ActividadesGuardadas(request):
    _list=[]
    _actividades = Generalidad_Tiempos.objects.all()
    for actividad in _actividades:
        _actividades_dic ={}
        _actividades_dic['id'] = actividad.id
        _actividades_dic['name'] = actividad.Actividad
        _list.append(_actividades_dic)
    data = json.dumps(_list)
    return HttpResponse(data, content_type = 'application/json')

def tiempo_actividades(request):
  _actividades = request.GET['actividades']
  _actividades_id = Generalidad_Tiempos.objects.filter( id = _actividades)
  data = serializers.serialize("json", _actividades_id)
  return HttpResponse(data, content_type='application/json') 

@csrf_exempt  #anti robots
def Maquinas_Y_Costos(request):
    _list =[]
    _maquinas = Maquina.objects.all()
    for maquina in _maquinas:
        _maquina_dic ={}
        _maquina_dic['id'] = maquina.id
        _maquina_dic['name'] = maquina.NombreRecurso
        _list.append( _maquina_dic)
    data = json.dumps(_list)
    return HttpResponse(data, content_type = 'application/json')
	
def Valor_Maquinas(request):
    _maquinas = request.GET['maquinas']
    _maquinas_id = Maquina.objects.filter(id = _maquinas)
    data = serializers.serialize("json",_maquinas_id )
    return HttpResponse(data, content_type='application/json')



	
	
def traerJornadas(request):
    _jornada_laboral = request.GET['id']
    _datos_jornada = Dia_Laboral.objects.filter(id =request.GET['id'])
    data = serializers.serialize("json", _datos_jornada)
    #data = json.dumps(_datos_jornada)
    return HttpResponse(data, content_type='application/json')

	

	
def Insertar_balanceo(request):
   _producto = request.GET['producto']
   _actividad=Generalidad_Tiempos.objects.get(id = request.GET['Actividad'])
   _tiempo_estandard = request.GET['Tieme']
   _maquina = Maquina.objects.get(id = request.GET['Insumos'])
   _costo_insumo =request.GET['costo_insumo']
   _lote = request.GET['Tieml']
   _recurso_humano = request.GET['rec']
   if _producto == "0":
      _balanceo = Producto_Referencia.objects.create()
   else:
      _balanceo = Producto_Referencia.objects.get(id=_producto)
   _balanceo_general= Ruta_Operacional.objects.create( Nombre_producto    = _balanceo , Actividad = _actividad ,Tiempo_Estandard= _tiempo_estandard ,  Maquina =_maquina, Precio = _costo_insumo,Recurso_humano =_recurso_humano, Tiempo_Lote = _lote ) 
   
   context = [{'balanceo_produccion_id':str(_balanceo_general), 'nuevo_balanceo_id':str(_balanceo.id),'result':'true'
   }]

   data = json.dumps(context)
   return HttpResponse(data, content_type='application/json')


def Actualizar_balanceo (request):
    _id = request.GET['id']
    _actividad=Generalidad_Tiempos.objects.get(id = request.GET['Act'])
    _maquina = Maquina.objects.get(id = request.GET['Insumos'])
    _costo_insumo =request.GET['costo_insumo']
    _lote = request.GET['tieml']
    _recurso_humano = request.GET['rec']	
    _tiempo_estandard = request.GET['tieme']
    _balanceo_general = Ruta_Operacional.objects.get(id=_id)
    _balanceo_general.Actividad = _actividad
    _balanceo_general.Maquina =_maquina
    _balanceo_general.Precio = _costo_insumo
    _balanceo_general.Tiempo_Lote =_lote
    _balanceo_general.Recurso_humano =_recurso_humano
    _balanceo_general.Tiempo_Estandard = _tiempo_estandard
    _balanceo_general.save()
    context = [{ 'balanceo_produccion_id': str(_balanceo_general), 'result': 'true'}]
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')
	
def Eliminar_balanceo (request):
    _id = request.GET['id']
    _balanceo_general = Ruta_Operacional.objects.get(id=_id)
    context = [{ 'eliminarRegistro': str(_balanceo_general), 'result': 'true'
    }]
    data = json.dumps(context)
    return HttpResponse(data, content_type='application/json')	
	
def generar_pdf(html):
    # Función para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result,encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


def modulo3_reporte(request, id_producto):
  balanceo =get_object_or_404(Producto_Referencia, id=id_producto)
  sumatorias =  Ruta_Operacional.objects.filter( Nombre_producto = balanceo.id)
  #return render(request,'web/ReporteBalanceo(beta).html',{'balanceo':  balanceo, 'sumatorias': sumatorias})
  html =  render_to_string('web/ReporteBalanceo.html',{'pagesize':'A4','balanceo':  balanceo, 'sumatorias': sumatorias}, context_instance=RequestContext(request))
  return generar_pdf(html)




 




	

	

