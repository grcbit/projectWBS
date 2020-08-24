# -*- coding: utf-8 -*-
import base64
demo = False

@auth.requires_login()
def projectWBS():
    db.Proyecto.id.readable=False
    links = [lambda row: A('Gantt',_class='button btn btn-danger',_href=URL("project","projectGantt", args=[row.id, base64.b64encode(str(row.Nombre))]))]
    if demo == False: 
        if (auth.has_membership(role='admin') or auth.has_membership(role='riskManager')):
            form = SQLFORM.grid(db.Proyecto, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
        else:
            form = SQLFORM.grid(db.Proyecto, links=links, searchable=True, create=False, editable=False, deletable=False, user_signature=True, paginate=10, maxtextlength=500)
            #redirect(URL('default','index'))
    elif demo == True:
        form = SQLFORM.grid(db.Proyecto, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    return dict(form=form)

@auth.requires_login()
def projectTask():
    db.Actividad.id.readable = False
    db.Actividad.pgroup.default = 0
    #db.Actividad.Visible.default = 'T'
    fields = (db.Actividad.ProyectoId, db.Actividad.edt, db.Actividad.pparent, db.Actividad.pgroup, db.Actividad.Actividad, db.Actividad.Descripcion, db.Actividad.Avance, db.Actividad.Visible)
    if demo == False:
        if (auth.has_membership(role='admin') or auth.has_membership(role='riskManager')):
            form = SQLFORM.grid(db.Actividad, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
        else:
            redirect(URL('default','index'))
    elif demo == True:
        form = SQLFORM.grid(db.Actividad, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    return dict(form=form)

@auth.requires_login()
def projectGantt():
    #if demo == False:
    #    if (auth.has_membership(role='admin') or auth.has_membership(role='riskManager')):
    #        pass
    #    else:
    #        redirect(URL('default','index'))
    titulo = base64.b64decode(request.args(1))
    tareas = db((db.Actividad.Visible=='T') & (db.Actividad.ProyectoId==request.args(0)) ).select(db.Actividad.ALL, orderby=db.Actividad.edt)
    entregable = db(db.Entregable).select(db.Entregable.ALL)
    tareasArreglo = []
    for i in tareas:
        tarea = []
        tarea.append(i.ProyectoId.Nombre)
        tarea.append(i.edt)
        tarea.append(i.Actividad)
        tarea.append(i.Descripcion)
        tarea.append(i.Responsable)
        tarea.append(i.Avance)
        tarea.append(i.FechaInicio)
        tarea.append(i.FechaFin)
        #tarea.append(i.Comentario)
        tarea.append(i.Pendiente)
        tarea.append(i.EnProgreso)
        tarea.append(i.Completado)
        #tareasArreglo.append(tarea)
        archivoEntregable = []
        archivoComentario = []
        for x in entregable:
            if x.ActividadId == i.id:
                archivo = URL('default/download', str(x.Archivo))
                archivoEntregable.append(archivo)
                archivoComentario.append(x.Comentario)
        tarea.append(archivoEntregable)
        tarea.append(archivoComentario)
        #archivoEntregable = []
        tareasArreglo.append(tarea)
    return dict(tareasArreglo=tareasArreglo, titulo=titulo, tareas=tareas)

@auth.requires_login()
def projectDeliverable():
    if demo == False:
        if (auth.has_membership(role='admin') or auth.has_membership(role='riskManager')):
            form = SQLFORM.grid(db.Entregable, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
        else:
            redirect(URL('default','index'))
    elif demo == True:
        form = SQLFORM.grid(db.Entregable, fields=fields, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500)
    return dict(form=form)
