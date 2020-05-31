from django.urls import path
from . import views 

app_name = 'app' 
urlpatterns = [
    path('', views.index, name='index'), 
    path('autenticar/', views.autenticar, name='autenticar'), 
    path('logout/', views.view_logout, name='view_logout'), 
    path('login/', views.form_login, name='form_login'),   
    path('registro/', views.form_registro, name='form_registro'),
    path('registrar/', views.registrar, name='registrar'), 
    path('crear-proyecto/', views.form_proyecto, name='form_proyecto'),
    path('proyecto/', views.proyecto, name='proyecto'),
    path('proyecto-editado/', views.proyecto2, name='proyecto2'),
    path('list-proyectos-creados/', views.list_proyectos_creados, name='list_proyectos_creados'),
    path('crear-tarea/', views.form_tarea, name='form_tarea'),
    path('tarea/', views.tarea, name='tarea'),
    path('agregar-developer/', views.form_agregar_developer, name='form_agregar_developer'),
    path('agrega_developer/', views.agrega_developer, name='agrega_developer'),
    path('ajax_developer/', views.ajax_developer, name='ajax_developer'),
    path('list-developer/', views.list_developer, name='list_developer'),
    path('cambio-estado/', views.cambio_estado, name='cambio_estado'),
    path('editar-proyecto/', views.form_proyecto2, name='form_proyecto2'),
    path('list-tareas-creadas/', views.list_tareas_creadas, name='list_tareas_creadas'),
    path('editar-tarea/', views.form_tarea2, name='form_tarea2'),
    path('tarea-editado/', views.tarea2, name='tarea2'),

]