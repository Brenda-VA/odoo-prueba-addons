/** @odoo-module **/

import { Component } from "@odoo/owl";
/* addons/owl_course/static/src/components/user/user_card.js */

/*  */
export class UserCard extends Component {
  //nombre de la clase
  static template = "owl_course.UserCard"; //nombre del xml q va a mostrar el contenido de esta clase (user_card.xml)
  /* Los props indican el tipo de dato que sí o sí necesita recibir este componente desde fuera para poder dibujarse
name DEBE ser un STRING, email DEBE ser un STRING y asi */
  static props = {
    name: String, //si no tiene 'optiona:' entonces es OBLIGATORIO
    email: String,
    role: { type: String, optional: true }, //parámetro optional en true significa q estos datos son opcionales, pueden o no llegar
    avatar: { type: String, optional: true },
  };

  //valores por defect
  static defaultProps = {
    role: "Usuario", //si no definimos un rol, se nos pondrá automaticamente como usuario
    avatar: "/web/static/img/default_icon_app.png", //valor por defecto del avatar si no ingresamos una imagen
  };
}
