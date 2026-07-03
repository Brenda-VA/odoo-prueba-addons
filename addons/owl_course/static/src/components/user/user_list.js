/** @odoo-module **/
/* addons/owl_course/static/src/components/user/user_list.js */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
//importamos la clase donde especificamos los props, es como el molde, sin ella Odoo no sabe como dibujar los datos de estos usuarios
//esta clase es un sub componente de esta, como el hijo
import { UserCard } from "./user_card";

export class UserList extends Component {
  //se pone el nombre de la plantilla q va a mostrar estos datos, user_list.xml -> t-name="owl_course.UserList"
  static template = "owl_course.UserList";
  static components = { UserCard }; //avisamos q dentro de la plantilla vamos a usar las etiquetas personalizadas de <UserCard />

  //método de iniciación de owl, se ejecuta 1 sola vez al momento exacto en q la pantalla se está cosntruyendo en el navegador
  setup() {
    //propiedad de clase que guarda un array de objetos, con esta informacion voy a renderizar una card
    this.users = [
      {
        name: "Juan Pérez",
        email: "juan.perez@example.com",
        role: "Administrador",
      },
      {
        name: "María López",
        email: "maria.lopez@example.com",
        role: "Usuario",
      },
      { name: "Carlos García", email: "carlos.garcia@example.com" }, //este usuario le falta rol pero no hay problema pq en la clase hijo   usamos defaultProps
      {
        name: "Ana Torres",
        email: "ana.torres@example.com",
        role: "Usuario",
      },
      {
        name: "Luis Fernández",
        email: "luis.fernandez@example.com",
        role: "Usuario",
      },
    ];
  }
}

// Registramos el componente user_list, el user_card no porque no es un componente como tal, es un sub componente de este
//guarda en la lista de registro de categorias por acción, el id de la acción es: "owl_course.user_list", nombre_modulo.nombre_archivo_javascript
registry.category("actions").add("owl_course.user_list", UserList); //el 2do parámetro es el nombre de la clase tal y como está
