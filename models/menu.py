# -*- coding: utf-8 -*-
response.menu = [
    (T('Home'), False, URL('default', 'index'), []),
    (T('Project'), False, '#', [
        #(T('Gantt'), False, URL('project', 'projectGantt')),
        (T('Project'), False, URL('project', 'projectWBS')),
        (T('Planner'), False, URL('project', 'projectTask')),
        (T('Deliverable'), False, URL('project', 'projectDeliverable')),
    ]),
    (T('License'), False, URL('default', 'license'), []),
]
