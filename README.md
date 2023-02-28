# Actividad Experiencia ADHOC

## Enunciado:

Un cliente de Adhoc tiene instalado el módulo real_state_management y notifican los siguientes errores y requerimientos:

1. El campo area total del inmueble no esta calculando el area correctamente.
2. El botón "Refuse Offer" muestra un error al intentar usarlo.
3. Quieren agregar un nuevo campo para "Tipo de Operacion", las opciones disponibles pueden ser Venta o Alquiler. No olvidar agregarlo en la vista formulario
4. Quieren agregar el campo "Tipo de Propiedad" en la vista lista y que se pueda agrupar

## Ejercicio:

1. Hacer fork de este repositorio (utilizar http para descargarlo en local)
2. Resolver el enunciado cada punto en un commit diferente.
3. Subir resultado a GitHub y pasarnos un correo con la url de tu fork/branch a bz@adhoc.com.ar

## Cómo levantar Odoo:

1. En una terminal nos dirigimos a la carpeta de odoo y luego a la versión que queremos ingresar, en este caso la versión 15. El comando a correr es

```
$ cd odoo/15
```
2. Luego se deberá correr el siguiente comando para levantar el contenedor de docker donde correrá nuestro odoo

```
$ docker-compose run --rm odoo bash
```
3. Por último vamos a correr odoo en el contenedor generando una nueva base para el ejercicio instalando la aplicación de real_state_management

```
$ odoo -d ejercicio_inmobiliaria -i real_state_management
```

4. Una vez corrido los comandos en un navegador ingresar la siguiente url: 15.odoo.localhost y tener en cuenta que tanto el usuario como contraseña de acceso es "admin".


## Cómo hacer modificaciones en el código:

1. Para cambios en archivo python (.py): bajar container (ctrl-c 2 veces) y volver a levantar al odoo. Para esto correr

```
$ odoo -d ejercicio_inmobiliaria
```

2. Para cambios en vistas (.xml):

```
$ odoo -d ejercicio_inmobiliaria --dev=xml
```

NOTA:

1. Para cuando vayan a hacer el primer commit te va a pedir que configures tu info. para ello puedes correr los siguentes pasos:

```
git config --global user.email <tu-email>
git config --global user.name <tu-number>
```

2. Este es el doc de referencia de ayuda de odoo https://www.odoo.com/documentation/15.0/developer/reference/backend/orm.html
