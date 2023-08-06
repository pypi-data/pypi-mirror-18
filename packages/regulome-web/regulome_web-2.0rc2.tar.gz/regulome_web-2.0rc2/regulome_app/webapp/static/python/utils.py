from browser import document, window


def redirect(ev):
    """Create the links"""
    document['navbar_link'].value = ev.target.id
    document['form_base'].action = 'submit'
    document['form_base'].submit()


def mark_as_active(pathname):
    """Mark the active page in the navbar"""
    for id_page in ('home', 'data', 'credits', 'contact', 'info'):
        if id_page in pathname:
            document[id_page].class_name = 'active'
        else:
            document[id_page].class_name = ''
    if 'show' in pathname:
        document['home'].class_name = 'active'


# This highlight the appropriate link in the navbar
mark_as_active(window.location.pathname)


# Events binding
document['home_main'].bind('click', redirect)
document['home'].bind('click', redirect)
document['data'].bind('click', redirect)
document['credits'].bind('click', redirect)
document['contact'].bind('click', redirect)
document['info'].bind('click', redirect)
