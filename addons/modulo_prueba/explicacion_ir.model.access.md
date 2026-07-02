**id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink**
**access_modulo_prueba_student,modulo_prueba.student,model_modulo_prueba_student,base.group_user,1,1,1,1**
**access_modulo_prueba_task,modulo_prueba.task,model_modulo_prueba_task,base.group_user,1,1,1,1**

#------ NINGUNA DE LAS FILAS DEBE TENER ESPACIOS ENTRE SUS ELEMENTOS ----------
#con esto se les da permisos a los usuarios para que puedan usar determinados modelos o evitar q miren infromación o tareas q no les pertenecen o crear un grupo personalizado para tener un administrador de tareas
#para cada modelo nuevo se debe de crear una línea nueva en: 'ir.model.access.csv'
#lo de arriba son los encabezados:

# id -- nombre -- id del modelo -- id del grupo -- permiso para leer -- permiso para escribir -- permiso para crear -- permiso para borrar

#abajo son los campos llenados

#'id': si en el modelo tenemos '\_name = "modulo_prueba.task"' entonces debe ir access_modulo_prueba_task o access_nombreModulo_nombreModelo
#'name': el mismo nombre que figura en \_name = "nombreModulo.nombreModelo" es decir 'modulo_prueba.task'
#'model_id:id': model_nombreModulo_nombreModelo y tmb sale de '\_name = "modulo_prueba.task"'
#'group_id:id': odoo les asigna de forma predeterminada 'base.group_user' a todos y significa usuarios internos de Odoo pero si se deja en blanco aplica a TODOS

# perm_read - perm_write - perm_create - perm_unlink: 1 es permitido y 0 es denegado

# PRIMERA CAPA DE SEGURIDAD: Con 'ir.model.access.csc' el usuario puede ENTRAR AL MODELO
# 2da CAPA DE SEGURIDAD: Con 'task_security.xml' el usuario puede ver solo los registros a los q tenga permitido acceder
task_security.xml ES DONDE SE DEFINNE LA REGLA DE Q LOS USUARIOS SOLO PUEDAN VER SUS PROPIAS TAREAS Y NO LA DE LOS DEMÁS 

ir.model.access.csv
↓
Permite entrar al edificio

ir.rule
↓
Permite entrar a determinadas habitaciones

--------  Entonces si he creado el modelo, la vista y el menú pero aún asi no puedo verlo quizás es pq me falta darle permisos en 'ir.model.access.csv' --------

