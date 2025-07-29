# Actividad Experiencia ADHOC

## Enunciado:

Un cliente de Adhoc tiene instalado el módulo real_state_management y notifican los siguientes errores y requerimientos:

1. El campo area total del inmueble no esta calculando el area correctamente.
2. El botón "Refuse Offer" devuelve un error.
3. Se solicita poder agrupar por el campo "Tipo de Propiedad" en la vista lista de propiedades.
4. Se solicita agregar los campos "Garage", que se pueda tildar para indicar que la propiedad tiene garage, y "Garage area", que permita indicar el area del garage y a su vez este contemplado en el área total del la propiedad. Los mismos se deben agregar en la vista formulario de las propiedades.
5. Implementación de Controladores (API/Endpoints)
  Desarrollar los siguientes endpoints:

  Endpoint 1: Listar propiedades no vendidas.
    Debe devolver información como:

      Nombre de la propiedad
      Vendedor
      Código postal
      Precio
      Metros cuadrados
      Otros campos relevantes

  Endpoint 2: Crear o actualizar una propiedad.
    Según el identificador recibido:
    Si la propiedad existe, actualizar algunos campos seleccionados (a elección).
    Si no existe, crear un nuevo registro con los datos provistos.

  Endpoint 3: Generar una oferta para una propiedad.
    Recibe como parámetro el identificador de la propiedad y los datos necesarios para completar la oferta.
    Debe devolver el mensaje: "Oferta creada" si la operación fue exitosa.

6. Desarrollo de Reporte de Propiedades Vendidas
Crear un reporte que muestre todas las propiedades vendidas en el último año, agrupadas por vendedor.

## Ejercicio:

1. Clonar este repositorio de manera local (utilizar http) en "~/odoo/16/data/custom/repositories"
2. Resolver el enunciado cada punto en un commit diferente.

## Cómo levantar Odoo:

1. En una terminal nos dirigimos a la carpeta de odoo y luego a la versión que queremos ingresar, en este caso la versión 16. El comando a correr es

```
$ cd odoo/16
```
2. Luego se deberá correr el siguiente comando para levantar el contenedor de docker donde correrá nuestro odoo

```
$ docker-compose run --rm odoo bash
```
3. Por último vamos a correr odoo en el contenedor generando una nueva base para el ejercicio instalando la aplicación de real_state_management

```
$ odoo -d ejercicio_inmobiliaria -i real_state_management
```

4. Una vez corrido los comandos en un navegador ingresar la siguiente url: [http://16.odoo.localhost](http://16.odoo.localhost) y tener en cuenta que tanto el usuario como contraseña de acceso es "admin".


## Cómo hacer modificaciones en el código:

1. Para cambios en archivo python (.py): bajar container (ctrl-c 2 veces) y volver a levantar al odoo. Para esto correr

```
$ odoo -d ejercicio_inmobiliaria
```

2. Para visualizar los cambios en vistas (.xml) sin necesidad de re-cargar odoo:

```
$ odoo -d ejercicio_inmobiliaria --dev=xml
```

3. Si se hacen modificaciones en la estructura de datos (campos y/o modelos), se debe recargar odoo llamando a actualizar el módulo. Por ej:
```
$ odoo -d ejercicio_inmobiliaria -u real_state_management
```

NOTA:

1. Para cuando vayan a hacer el primer commit te va a pedir que configures tu info. para ello puedes correr los siguentes pasos:

```
git config --global user.email <tu-email>
git config --global user.name <tu-nombre>
```

2. Este es el doc de referencia de ayuda de odoo https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html
