from browser import document, alert


def assign_value_to_navbar_link(ev):
    """Assign the 'home' value to the navbar_link"""
    document['navbar_link'].value = 'home'


def button_controls(ev):
    """Submit the form after one of the control links has been clicked"""
    document['loader'].style.display = 'block'
    document['download'].value = ''
    document['form_base'].action = 'submit'
    document['form_base'].submit()


def button_download(ev):
    """Submit the form after one of the download links has been clicked"""
    document['download'].value = ev.target.id
    document['form_base'].action = 'downloads'
    document['form_base'].submit()


def button_submit(ev):
    """Submit the form to do another plot"""
    assign_value_to_navbar_link(ev)
    document['loader'].style.display = 'block'
    document['download'].value = ''
    document['form_base'].action = 'submit'
    document['form_base'].submit()


# Events binding
document['submit_button_plot'].bind('click', button_submit)

for element_id in (
        "zoom_in_1.5x", "zoom_in_3x", "zoom_in_10x",
        "zoom_out_1.5x", "zoom_out_3x", "zoom_out_10x",
        "left_25", "left_50", "left_75",
        "right_25", "right_50", "right_75"):
    document[element_id].bind('click', button_controls)

for element_id in (
        'download_pdf', 'download_png',
        'download_table', 'download_snps'):
    try:
        document[element_id].bind('click', button_download)
    except KeyError as e:
        # The element does not exist
        pass
