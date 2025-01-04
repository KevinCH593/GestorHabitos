from django.shortcuts import render, redirect, get_object_or_404
from .models import Habitos, RegistroInicio

# Importar libreria para manejar fechas
from datetime import date

#Importar libreria para respuesta Json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
#Importar libreria para mensajes de confirmacion
from django.contrib import messages

################################################################
# INDEX
################################################################
# Página principal: lista de hábitos y progreso
def inicio(request):
    # Filtrar hábitos activos
    habitos = Habitos.objects.filter(estado=True)
    
    # Calcular estadísticas
    total_habitos = habitos.count()
    
    return render(request, 'index.html', {
        'habits': habitos,
        'total_habitos': total_habitos
    })
# Crear un nuevo hábito
def crear_habito(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        try:
            meta_horas = int(request.POST.get('meta_horas', 0))
            meta_minutos = int(request.POST.get('meta_minutos', 0))
            if meta_horas < 0 or meta_minutos < 0 or meta_minutos >= 60:
                raise ValueError("Horas o minutos inválidos.")
            meta_tiempo = meta_horas * 60 + meta_minutos
        except ValueError:
            return render(request, 'crear_habito.html')

        prioridad = request.POST.get('prioridad')

        Habitos.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            meta_tiempo=meta_tiempo,
            prioridad=prioridad
        )
        messages.success(request,'Hábito creado exitosamente')
        return redirect('inicio')

    return render(request, 'crear_habito.html')

# Actualizar un hábito
def actualizar_habito(request, pk):
    habito = get_object_or_404(Habitos, pk=pk)
    # Cálculos para pasar horas y minutos al contexto
    meta_horas = habito.meta_tiempo // 60
    meta_minutos = habito.meta_tiempo % 60
    if request.method == 'POST':
        habito.nombre = request.POST['nombre']
        habito.descripcion = request.POST.get('descripcion', '')
        meta_horas = int(request.POST.get('meta_horas', 0))
        meta_minutos = int(request.POST.get('meta_minutos', 0))
        habito.meta_tiempo = meta_horas * 60 + meta_minutos
        habito.prioridad = request.POST['prioridad']
        habito.save()
        messages.success(request,'Hábito editado exitosamente')
        return redirect('inicio')
    return render(request, 'actualizar_habito.html', {
        'habito': habito,
        'meta_horas': meta_horas,
        'meta_minutos': meta_minutos,
    })
# Eliminar un hábito
def eliminar_habito(request, pk):
    habito = get_object_or_404(Habitos, pk=pk)  # Usa Habitos
    if request.method == 'POST':
        habito.delete()
        messages.success(request,'Hábito eliminado exitosamente')
        return redirect('inicio')
    return redirect('inicio')

# Vista para iniciar un hábito
def iniciar_habito(request):
    if request.method == "POST":
        try:
            print("Cuerpo de la solicitud:", request.body)  # Registro para depurar
            data = json.loads(request.body)  # Carga el cuerpo como JSON
            print("Datos recibidos:", data)

            habito_id = data.get('habito_id')  # Obtiene el `habito_id`
            print(f"ID del hábito recibido: {habito_id}")

            if not habito_id:
                print("ID del hábito no proporcionado.")
                return JsonResponse({'error': 'El ID del hábito es requerido.'}, status=400)
            
            habito = get_object_or_404(Habitos, pk=habito_id)
            print(f"Hábito encontrado: {habito}")

            registro = RegistroInicio.objects.create(habito=habito)
            print(f"Registro creado: {registro}")

            return JsonResponse({
                'message': f"Inicio del hábito '{habito.nombre}' registrado correctamente.",
                'registro_id': registro.id,
                'fecha_inicio': registro.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            })
        except Exception as e:
            print(f"Error en la vista: {e}")
            return JsonResponse({'error': f"Error inesperado: {str(e)}"}, status=500)
    print("Método no permitido")
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def detalle_habito(request, pk):
    habito = get_object_or_404(Habitos, pk=pk)
    registros = habito.registros.all()
    return render(request, 'detalle_habito.html', {
        'habito': habito,
        'registros': registros
    })
def obtener_registros(request, habito_id):
    habito = Habitos.objects.get(id=habito_id)
    registros = habito.registros.all().values(
        'id', 'fecha_inicio', 'tiempo_transcurrido', 'completado'
    )
    return JsonResponse(list(registros), safe=False)

    
def completar_registro(habito_id):
    habito = Habitos.objects.get(id=habito_id)
    registro = habito.registros.filter(completado=False).last()  # Asumiendo que buscas el último registro no completado

    if registro:
        registro.completado = True
        registro.tiempo_transcurrido = habito.meta_tiempo  # O cualquier valor que corresponda al tiempo completado
        registro.save()

        # Otras acciones (por ejemplo, notificar al cliente)
        return registro

def completar_habito(request, habito_id):
    try:
        # Obtener el hábito
        habito = Habitos.objects.get(id=habito_id)

        # Obtener el último registro asociado con el hábito que no esté completado
        registro = habito.registros.filter(completado=False).last()

        if registro:
            # Si se encuentra un registro no completado, actualizamos los campos
            registro.completado = True
            registro.tiempo_transcurrido = habito.meta_tiempo  # O el tiempo actual que se haya alcanzado
            registro.save()

            # Devolver los datos actualizados
            return JsonResponse({
                'status': 'success',
                'message': 'Hábito completado',
                'registro': {
                    'id': registro.id,
                    'fecha_inicio': registro.fecha_inicio,
                    'tiempo_transcurrido': registro.tiempo_transcurrido,
                    'completado': registro.completado
                }
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'No se encontró un registro no completado'})
    except Habitos.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Hábito no encontrado'})