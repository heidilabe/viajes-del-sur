from django.db import models


class Persona(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    foto = models.ImageField(upload_to='personas/', null=True, blank=True)

    class Meta:
        ordering = ['apellido', 'nombre']
        verbose_name = 'persona'
        verbose_name_plural = 'personas'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Lugar(models.Model):
    nombre = models.CharField(max_length=150)
    pais = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='lugares/', null=True, blank=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'lugar'
        verbose_name_plural = 'lugares'

    def __str__(self):
        return f"{self.nombre} ({self.ciudad}, {self.pais})"


class Viaje(models.Model):
    ESTRELLAS = [(i, f"{i} Estrellas") for i in range(1, 6)]

    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name='viajes',
        verbose_name='persona',
    )
    lugar = models.ForeignKey(
        Lugar,
        on_delete=models.CASCADE,
        related_name='viajes',
        verbose_name='lugar',
    )
    fecha_visita = models.DateField('fecha de visita')
    titulo = models.CharField('título', max_length=200)
    relato = models.TextField('relato')
    foto = models.ImageField(upload_to='viajes/', null=True, blank=True)
    calificacion = models.IntegerField('calificación', choices=ESTRELLAS)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'viaje'
        verbose_name_plural = 'viajes'

    def __str__(self):
        return f"{self.titulo} - {self.persona}"
