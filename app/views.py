from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from app.models import Proyecto,Developer,Estado,Tarea
from django.core import serializers
import json

	
@login_required
def index(request):
    return render(request, "app/index.html")  

def form_login(request):
    mensaje=""
    alertError=False

    contexto = { 
        'mensaje': mensaje,
        'alertError':alertError         
    }

    return render(request, "app/login.html",contexto)    

def form_registro(request):
    return render(request, "app/registrar.html")      

def registrar(request):
    mensaje=""
    alertOk=False
    alertError=False

     # Obtiene los datos
    username = request.POST['username']
    nombres = request.POST['nombres']
    email = request.POST['email']
    password = request.POST['password']
    apellidos = request.POST['apellidos']

    usuarioAux=User.objects.filter(Q(username=username) | Q(email=email))

    if not usuarioAux :
        # Crea el objeto usuario
        usuario = User(username=username, first_name=nombres, email=email, last_name=apellidos)
        usuario.set_password(password)
 
        # Guarda el usuario en la base de datos
        usuario.save()

        mensaje="El usuario fue registrado exitosamente"
        alertOk=True
    else: 
        mensaje="Hay un usuario con el mismo username o email registrado"
        alertError=True

    contexto = { 
        'mensaje': mensaje,
        'alertOk':alertOk,
        'alertError':alertError         
    }
    

    return render(request, "app/registrar.html",contexto) 

def view_logout(request):
  # Cierra la sesión del usuario
  logout(request)

  # Redirecciona la página de login
  return redirect('app:form_login')

def autenticar(request):
    # Obtiene los datos del formulario de autenticación
    username = request.POST['username']
    password = request.POST['password']
 
    # Obtiene el usuario
    usuario = authenticate(username=username, password=password)
 
    # Verifica si el usuario existe en la base de datos 
    if usuario is not None:
        # Inicia la sesión del usuario en el sistema
        login(request, usuario)
        # Redirecciona a una página de éxito
        return redirect('app:index')
    else:
        # Retorna un mensaje de error de login no válido
        mensaje="Username o Password incorrecto"
        alertError=True

        contexto = { 
            'mensaje': mensaje,
            'alertError':alertError         
        }
        return render(request, 'app/login.html',contexto) 

@login_required
def form_proyecto(request):
    return render(request, "app/proyecto.html") 

@login_required
def form_proyecto2(request):
    idProyecto= request.POST['idProyecto']

    proyecto=Proyecto()
    
    if idProyecto:
        proyecto=Proyecto.objects.get(id=int(idProyecto))


    contexto = { 
        'proyecto': proyecto 
    } 

    return render(request, "app/editar_proyecto.html",contexto)   

@login_required
def proyecto(request):
    mensaje=""
    alertError=False
    alertOk=False

    nombre=request.POST['nombre']
    descripcion=request.POST['descripcion']

    proyecto=Proyecto.objects.filter(nombre=nombre)

    if proyecto:
        mensaje = "Este nombre ya esta asignado"
        alertError =True    
    else:
        proyecto=Proyecto()
        proyecto.nombre=nombre
        proyecto.descripcion=descripcion

        productOwner=User.objects.get(id=request.user.id)
        proyecto.productOwner=productOwner 

        proyecto.save()

        mensaje="El proyecto fue creado exitosamente"
        alertOk=True

    contexto = { 
        'mensaje': mensaje,
        'alertOk':alertOk,   
        'alertError':alertError
    } 

    return render(request, "app/proyecto.html",contexto)     

@login_required
def proyecto2(request):

    idProyecto= request.POST['idProyecto']
    descripcion=request.POST['descripcion']

    proyecto=Proyecto.objects.get(id=int(idProyecto))

    proyecto.descripcion=descripcion

    productOwner=User.objects.get(id=request.user.id)
    proyecto.productOwner=productOwner 

    proyecto.save()

    return redirect("app:list_proyectos_creados")      

@login_required
def list_proyectos_creados(request):

    productOwner=User.objects.get(id=request.user.id)
    lista_proyectos=Proyecto.objects.filter( productOwner=productOwner)
    
    contexto = { 
        'lista_proyectos': lista_proyectos         
    } 

    return render(request, "app/proyectos_creados.html",contexto)      

@login_required
def form_tarea(request):

    productOwner=User.objects.get(id=request.user.id)
    lista_proyectos=Proyecto.objects.filter( productOwner=productOwner)
    
    contexto = { 
        'lista_proyectos': lista_proyectos,   
    } 

    return render(request, "app/tarea.html",contexto)      


@login_required
def form_agregar_developer(request):

    list_usuarios=User.objects.all()

    productOwner=User.objects.get(id=request.user.id)
    lista_proyectos=Proyecto.objects.filter( productOwner=productOwner)
    
    contexto = { 
        'lista_proyectos': lista_proyectos,   
        'lista_usuarios': list_usuarios      
    } 

    return render(request, "app/agregar_developer.html",contexto)   


@login_required
def agrega_developer(request):

    mensaje=""
    alertOk=False
    alertError=False

    list_usuarios=User.objects.all()

    productOwner=User.objects.get(id=request.user.id)
    lista_proyectos=Proyecto.objects.filter( productOwner=productOwner)

    idProyecto = request.POST['proyecto']
    idUsuario = request.POST['usuario']

    proyecto=Proyecto.objects.get(id=idProyecto)
    usuario=User.objects.get(id=idUsuario)

    developer=Developer.objects.filter(Q(idUser=usuario) & Q(idProyecto=proyecto))

    if not developer:
        developer=Developer()
        developer.idProyecto=proyecto
        developer.idUser=usuario
        developer.activo='A'
        developer.save()

        mensaje="El usuario fue agregado exitosamente"
        alertOk=True
    else:
        mensaje="El usuario ya estaba agregado"
        alertError=True
    
    contexto = { 
        'lista_proyectos': lista_proyectos,   
        'lista_usuarios': list_usuarios,
        'mensaje': mensaje,
        'alertOk':alertOk,
        'alertError':alertError       
    } 

    return render(request, "app/agregar_developer.html",contexto) 


@login_required
def ajax_developer(request):
    idProyecto=request.GET['idProyecto']
    proyecto=Proyecto.objects.get(id=idProyecto)
    developers=Developer.objects.filter(idProyecto=proyecto)
    developers=[ developer_serializer(data) for data in developers ]  

    return HttpResponse(json.dumps(developers),content_type='application/json') 

def developer_serializer(data):    
    usuario=User.objects.get(id=data.idUser_id)
    return {'id':usuario.id,'username':usuario.username}


@login_required
def tarea(request):
    mensaje=""
    alertOk=False

    nombre=request.POST['nombre']
    descripcion=request.POST['descripcion']
    idProyecto=request.POST['proyecto']
    idDeveloper=request.POST['developer']
    tiempoEstimado=request.POST['tiempoEstimado']

    productOwner=User.objects.get(id=request.user.id)
    lista_proyectos=Proyecto.objects.filter( productOwner=productOwner)

    estado=Estado.objects.get(nombre='To Do')

    if not estado:
        estado=Estado()
        estado.nombre="To Do"
        estado.save()

    tarea=Tarea()
    tarea.nombre=nombre
    tarea.descripcion=descripcion
    tarea.proyecto=Proyecto.objects.get( id=idProyecto)
    if idDeveloper:
        tarea.developer=User.objects.get(id=idDeveloper)
    tarea.estadoActual=Estado.objects.get(nombre='To Do')
    tarea.tiempoEstimado=tiempoEstimado
    tarea.save()

    mensaje="La tarea fue creada exitosamente"
    alertOk=True
    
    contexto = { 
        'lista_proyectos': lista_proyectos,
        'mensaje': mensaje,
        'alertOk':alertOk   
   } 

    return render(request, "app/tarea.html",contexto) 

@login_required
def list_developer(request):

    productOwner=User.objects.get(id=request.user.id)
    lista_proyectos=Proyecto.objects.filter( productOwner=productOwner)

    lista_developer=Developer.objects.filter( idProyecto__in=[p.id for p in lista_proyectos])
       
    contexto = { 
        'lista_developer': lista_developer        
    } 

    return render(request, "app/developer_proyecto.html",contexto)    

@login_required
def cambio_estado(request):
    mensaje=""
    alertOk=False

    productOwner=User.objects.get(id=request.user.id)
    lista_proyectos=Proyecto.objects.filter( productOwner=productOwner)

    lista_developer=Developer.objects.filter( idProyecto__in=[p.id for p in lista_proyectos])

    idDeveloper= int(request.POST['idDeveloper'])
    estado=request.POST['estado']

    developer=Developer.objects.get(id=idDeveloper)

    if estado in 'A':
        developer.activo='I'
    else:
        developer.activo='A'  

    developer.save()

    mensaje="El cambio de estado fue exitosamente"
    alertOk=True 

    contexto = { 
        'lista_developer': lista_developer,
        'mensaje': mensaje,
        'alertOk':alertOk          
    } 


    return render(request, "app/developer_proyecto.html",contexto)


@login_required
def list_tareas_creadas(request):

    productOwner=User.objects.get(id=request.user.id)
    lista_proyectos=Proyecto.objects.filter( productOwner=productOwner)

    lista_tareas=Tarea.objects.filter( proyecto__in=[p.id for p in lista_proyectos])

    
    contexto = { 
        'lista_tareas': lista_tareas         
    } 

    return render(request, "app/tareas_creadas.html",contexto)  

@login_required
def form_tarea2(request):

    idTarea= request.POST['idTarea']

    tarea=Tarea()
    
    if idTarea:
        tarea=Tarea.objects.get(id=int(idTarea))


    productOwner=User.objects.get(id=request.user.id)
    lista_proyectos=Proyecto.objects.filter( productOwner=productOwner)
    
    contexto = { 
        'lista_proyectos': lista_proyectos, 
        'tarea' :tarea 
    } 

    return render(request, "app/editar_tarea.html",contexto)  

@login_required
def tarea2(request):
    
    idTarea= request.POST['idTarea']
    descripcion=request.POST['descripcion']
    idProyecto=request.POST['proyecto']
    idDeveloper=request.POST['developer']
    tiempoEstimado=request.POST['tiempoEstimado']

    productOwner=User.objects.get(id=request.user.id)
  
    # estado=Estado.objects.get(nombre='To Do')

    # if not estado:
    #     estado=Estado()
    #     estado.nombre="To Do"
    #     estado.save()

    tarea=Tarea.objects.get(id=int(idTarea))
    tarea.descripcion=descripcion
    tarea.proyecto=Proyecto.objects.get( id=idProyecto)
    if idDeveloper:
        tarea.developer=User.objects.get(id=idDeveloper)
    # tarea.estadoActual=Estado.objects.get(nombre='To Do')
    tarea.tiempoEstimado=tiempoEstimado
    tarea.save()

    return redirect("app:list_tareas_creadas") 