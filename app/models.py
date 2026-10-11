from decimal import Decimal

from django.db import models


class Asignatura(models.Model):
    codigo = models.CharField('código', max_length=10, unique=True)
    nombre = models.CharField('nombre', max_length=120)
    creditos = models.PositiveIntegerField('créditos', default=7)
    descripcion = models.TextField('descripción', blank=True)
    creada_en = models.DateTimeField('creada el', auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'asignatura'
        verbose_name_plural = 'asignaturas'

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Estudiante(models.Model):
    rut = models.CharField('RUT', max_length=12, unique=True)
    nombres = models.CharField('nombres', max_length=80)
    apellidos = models.CharField('apellidos', max_length=80)
    correo = models.EmailField('correo electrónico', blank=True)
    fecha_nacimiento = models.DateField('fecha de nacimiento', null=True, blank=True)
    asignaturas = models.ManyToManyField(
        Asignatura,
        verbose_name='asignaturas',
        related_name='estudiantes',
        blank=True,
    )
    creado_en = models.DateTimeField('creado el', auto_now_add=True)

    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'estudiante'
        verbose_name_plural = 'estudiantes'

    def __str__(self):
        return f'{self.apellidos}, {self.nombres} ({self.rut})'


class Evaluacion(models.Model):
    class Tipo(models.TextChoices):
        TAREA = 'TAREA', 'Tarea'
        PRUEBA = 'PRUEBA', 'Prueba'
        EXAMEN = 'EXAMEN', 'Examen'
        PROYECTO = 'PROYECTO', 'Proyecto'

    asignatura = models.ForeignKey(
        Asignatura,
        verbose_name='asignatura',
        on_delete=models.CASCADE,
        related_name='evaluaciones',
    )
    titulo = models.CharField('título', max_length=120)
    tipo = models.CharField('tipo', max_length=10, choices=Tipo.choices, default=Tipo.TAREA)
    fecha = models.DateTimeField('fecha y hora')
    puntaje_maximo = models.DecimalField(
        'puntaje máximo',
        max_digits=5,
        decimal_places=2,
        default=Decimal('100.00'),
    )
    ponderacion = models.DecimalField(
        'ponderación (%)',
        max_digits=5,
        decimal_places=2,
        default=Decimal('25.00'),
    )
    instrucciones = models.TextField('instrucciones', blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'evaluación'
        verbose_name_plural = 'evaluaciones'

    def __str__(self):
        return f'{self.titulo} ({self.get_tipo_display()}) - {self.asignatura}'


class Calificacion(models.Model):
    evaluacion = models.ForeignKey(
        Evaluacion,
        verbose_name='evaluación',
        on_delete=models.CASCADE,
        related_name='calificaciones',
    )
    estudiante = models.ForeignKey(
        Estudiante,
        verbose_name='estudiante',
        on_delete=models.CASCADE,
        related_name='calificaciones',
    )
    puntaje = models.DecimalField('puntaje', max_digits=5, decimal_places=2)
    observaciones = models.CharField('observaciones', max_length=255, blank=True)
    registrada_en = models.DateTimeField('registrada el', auto_now_add=True)

    class Meta:
        ordering = ['evaluacion', 'estudiante']
        verbose_name = 'calificación'
        verbose_name_plural = 'calificaciones'
        constraints = [
            models.UniqueConstraint(
                fields=['evaluacion', 'estudiante'],
                name='calificacion_unica_por_evaluacion_y_estudiante',
            ),
            models.CheckConstraint(
                condition=models.Q(puntaje__gte=0),
                name='calificacion_puntaje_no_negativo',
            ),
        ]

    def __str__(self):
        return f'{self.estudiante} - {self.evaluacion}: {self.puntaje}'
