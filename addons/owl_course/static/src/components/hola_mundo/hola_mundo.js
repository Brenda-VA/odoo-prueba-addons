/** @odoo-module **/
/* addons/owl_course/static/src/components/hola_mundo/hola_mundo.js */

/* Tod_o en Odoo es un componente y fueron diseñadps especifícamente para Odoo, 
son reactivos por lo que se actualizaran automaticamente en cuanto cambien sus datos
Todos heredan de la clase Component*/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class HelloWorld extends Component {
  /* Propiedad estática 'template': Define la representacion visual del componente
    static template = "nombre_módulo.nombre_xmlQueVaAtenerLaVista";*/
  static template = "owl_course.HelloWorld";
}

/*'registry...': Sirve para registrar el componente en algua de las categorias de Odoo para q este se entere de q existe y lo muestre
  .category("actions"): almacena las acciones del cliente (pantallas que se disparan cuando un usuario hace clic en un menú)                                                        */
registry.category("actions").add(
  /* nomeclatura: nombre_modulo.nombre_accion */
  "owl_course.hello_world" /*--> Clave ID, nombre técnico que se va a colocar en 'name="tag"' del XML*/,
  HelloWorld /*--> Clase que tiene la lógica q se va a ejecutar cuando alguien dispare la acción, nombre_clase_javascript (línea 11) */,
);
