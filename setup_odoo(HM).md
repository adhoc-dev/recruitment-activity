# Para Hiring Managers

## Cómo levantar Odoo:

1. En una terminal nos dirigimos a la carpeta de odoo y luego a la versión que queremos ingresar, en este caso la versión 18. El comando a correr es

```
cd odoo/18
```
2. Luego se deberá correr el siguiente comando para levantar el contenedor de docker donde correrá nuestro odoo

```
docker-compose run --rm odoo bash
```
3. Por último vamos a correr odoo en el contenedor generando una nueva base para el ejercicio instalando la aplicación de real_state_management

```
odoo -d ejercicio_inmobiliaria -i real_state_management
```

4. Una vez corrido los comandos en un navegador ingresar la siguiente url: [http://18.odoo.localhost](http://18.odoo.localhost) y tener en cuenta que tanto el usuario como contraseña de acceso es "admin".
