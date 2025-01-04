from django.urls import path
from . import views

urlpatterns = [
    # URL INDEX
    path('', views.inicio, name='inicio'),
    
    # URL para iniciar hábito
    path('iniciar_habito/<int:pk>/', views.iniciar_habito, name='iniciar_habito'),

    # URL HABITOS
    path('crear/', views.crear_habito, name='crear_habito'),
    path('<int:pk>/actualizar/', views.actualizar_habito, name='actualizar_habito'),
    path('<int:pk>/eliminar/', views.eliminar_habito, name='eliminar_habito'),

    path('detalle_habito/<int:pk>/', views.detalle_habito, name='detalle_habito'),
    path('iniciar_habito/', views.iniciar_habito, name='iniciar_habito'),

    path('obtener_registros/<int:habito_id>/', views.obtener_registros, name='obtener_registros'),


]
