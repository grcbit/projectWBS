# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
import base64
# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)
#auth.define_tables(username=True)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
db.define_table('Proyecto',
    Field('Nombre','string', label=T('NAME')),
    Field('Objetivo','text', label=T('OBJECTIVE')),
    #Field('Descripcion', 'text', label=T('DESCRIPTION')),
    Field('FechaInicio', 'date', label=T('START DATE'), default=request.now),
    #Field('FechaInicio', 'date', label=T('START DATE'), default=request.now, requires = IS_DATE(format=('%d/%m/%Y'))),
    #Field('FechaInicio', 'date', label=T('START DATE'), default=request.now, requires = IS_DATE(format=('%Y-%m-%d'))),
    Field('FechaFin', 'date', label=T('END DATE')),
    #Field('FechaFin', 'date', label=T('END DATE'), requires = IS_DATE(format=('%d/%m/%Y'))),
    #Field('FechaFin', 'date', label=T('END DATE'), requires = IS_DATE(format=('%Y-%m-%d'))),
    Field('Documento', 'upload', label=T('DOCUMENT')),
    #Field('Visible', 'boolean', label=T('VISIBLE') ),
    format=lambda r: '%s' % (r.Nombre)
    )

db.define_table('Actividad',
    Field('ProyectoId', 'reference Proyecto', label=T('PROJECT')),
    Field('edt', 'integer', label=T('EDT'), comment=T('A unique numeric ID')),                                                   #pID
    Field('pgroup', 'integer', label=T('GROUP'), default=1, comment=T('Indicates whether this is a group task (parent). 0=task, 1=group task, 2=combined, 3=milestone')),#pGroup
    Field('popen', 'integer', label=T('GROUP OPEN'), default=0, comment=T('Indicates whether a standard group task is open when chart is first drawn. Value must be set for all items but is only used by standard group tasks. Numeric, 1 = open, 0 = closed')),#pGroup
    Field('pparent', 'integer', label=T('PARENT'), default=0, comment=T('Identifies a parent pID, this causes this task to be a child of identified task. Numeric, top level tasks should have pParent set to 0')),                                            #pParent-identifies a parent pID
    Field('depend', 'string', label=T('DEPEND'), comment=T('FS-Finish to Start, SF-Start to Finish, SS-Start to Start, FF-Finish to Finish')),                                                                                        #FS,SF,SS,FF
    Field('Actividad', 'string', label=T('ACTIVITY')),                                        #pName
    Field('Descripcion', 'string', label=T('ACTIVITY DESCRIPTION'), comment=T('Do not carriage return')),
    Field('Responsable', 'string', label=T('RESPONSIBLE')),
    Field('Avance', 'integer', label = T('PROGRESS %'), default=0),                                       #pComp - completion percent, numeric
    Field('FechaInicio', 'date', label = T('START DATE'), default=request.now),                                   #pStart
    #Field('FechaInicio', 'date', label = T('START DATE'), default=request.now, requires = IS_DATE(format=('%d/%m/%Y'))),                                   #pStart
    #Field('FechaInicio', 'date', label = T('START DATE'), default=request.now, requires = IS_DATE(format=('%Y-%m-%d'))),                                   #pStart
    Field('FechaFin', 'date', label=T('END DATE'), default=request.now),                                          #pEnd:
    #Field('FechaFin', 'date', label=T('END DATE'), requires = IS_DATE(format=('%d/%m/%Y'))),                                          #pEnd:
    #Field('FechaFin', 'date', label=T('END DATE'), requires = IS_DATE(format=('%Y-%m-%d'))),                                          #pEnd:
    #Field('Comentario', 'text', label=T('COMMENTS')),
    Field('Evidencia', 'upload', label=T('EVIDENCE')),
    Field('Visible', 'boolean', label=T('VISIBLE')),
    Field('Milestone', 'boolean', label=T('MILESTONE'), comment=T('Indicates whether this is a milestone task - Numeric; 1 = milestone, 0 = not milestone')),                                      #pMile
    Field('TaskColor', 'string', label=T('TASK COLOR')),
    Field('Pendiente', 'text', label=T('TO DO')),
    Field('EnProgreso', 'text', label=T('DOING')),
    Field('Completado', 'text', label=T('DONE')),
    format=lambda r: '%s %s %s %s %s %s %s' % (r.ProyectoId.id, '|', r.ProyectoId.Nombre, '|', r.edt, '|', r.Actividad),
    )
db.Actividad.edt.requires=IS_NOT_IN_DB(db( (db.Actividad.ProyectoId==request.vars.ProyectoId) ), db.Actividad.edt)
#db.Actividad.pgroup.requires=IS_IN_SET(['0','1','2','3'])
db.Actividad.pgroup.requires=IS_IN_SET([('0','Task'),('1','Group Task'),('2','Combined'),('3','Milestone')])
#db.Actividad.popen.requires =IS_IN_SET(['0','1'])
db.Actividad.popen.requires =IS_IN_SET([('0', 'Closed'),('1','Open')])
db.Actividad.Visible.default = 'T'
db.Actividad.TaskColor.default = 'blue'
db.Actividad.TaskColor.requires=IS_IN_SET(['blue','red','yellow', 'pink', 'purple', 'green'])
#db.Actividad.pparent.requires = IS_IN_DB(db(db.Actividad.pgroup==1), db.Actividad.edt, '%(edt)s %(Actividad)s')

db.define_table('Entregable',
    Field('ActividadId', 'reference Actividad', label=T('ACTIVITY')),
    Field('Archivo', 'upload', label=T('FILE')),
    Field('Comentario', 'text', label=T('COMMENTS')),
    )
