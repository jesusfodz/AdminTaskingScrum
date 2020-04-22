from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=45, null=False)
    first_name = models.CharField(max_length=45, null=False)
    last_name = models.CharField(max_length=45, null=False)
    email = models.CharField(max_length=45, null=False)
    password = models.CharField(max_length=45, null=False)
 
    def __str__(self):
        return self.email
 
    class Meta:
        app_label = 'app'

class Estado(models.Model):
    nombre = models.CharField(max_length=45, null=False)
 
    def __str__(self):
        return self.nombre
 
    class Meta:
        app_label = 'app'

class Proyecto(models.Model):
    nombre = models.CharField(max_length=45, null=False)
    descripcion = models.CharField(max_length=45, null=False)
    productOwner =models.ForeignKey(User,
                  related_name='productOwner',
                  null=False,                  
                  on_delete=models.PROTECT)
 
    def __str__(self):
        return self.nombre
 
    class Meta:
        app_label = 'app'      

  
class Developer(models.Model):
    activo = models.CharField(max_length=1, null=False)
    idUser =models.ForeignKey(User,
                  related_name='idUser',
                  null=False,                  
                  on_delete=models.PROTECT)
    idProyecto =models.ForeignKey(Proyecto,
                  related_name='idProyecto',
                  null=False,                  
                  on_delete=models.PROTECT)
 
    def __str__(self):
        return self.activo
 
    class Meta:
        app_label = 'app' 

class Tarea(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.TextField(null=True)
    tiempoEstimado = models.IntegerField(null=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    developer =models.ForeignKey(User,
                  related_name='developer',
                  null=True,                  
                  on_delete=models.PROTECT)
    proyecto =models.ForeignKey(Proyecto,
                  related_name='proyecto',
                  null=False,                  
                  on_delete=models.PROTECT)
    estadoActual =models.ForeignKey(Estado,
                  related_name='estadoActual',
                  null=False,                  
                  on_delete=models.PROTECT)
 
    def __str__(self):
        return self.nombre
 
    class Meta:
        app_label = 'app' 

class Avance(models.Model):
    descripcion = models.TextField(null=True)
    tiempoTrabajado = models.IntegerField(null=False)
    tiempoRestante = models.IntegerField(null=False)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario =models.ForeignKey(User,
                  related_name='usuario',
                  null=False,                  
                  on_delete=models.PROTECT)
    tarea =models.ForeignKey(Tarea,
                  related_name='tarea',
                  null=False,                  
                  on_delete=models.PROTECT)
 
    def __str__(self):
        return self.descripcion
 
    class Meta:
        app_label = 'app' 