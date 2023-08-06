from browser import document, window, alert


panels = (
    'info_create_plot',
    'info_plot_description',
    'info_moving_around',
    'info_upload_your_data',
    'info_retrieve_results'
)


def toggle_panel(hash):
    """Open and close the main panels"""
    for panel in panels:
        if panel == hash:
            document[panel].class_name = 'panel-collapse collapse in'
            document[panel + "_icon"].class_name = 'heading-advanced-icon'
        else:
            document[panel].class_name = 'panel-collapse collapse'
            document[panel + "_icon"].class_name = 'heading-advanced-icon collapsed'


def collapse_in():
    """Open a collapsed panel"""
    hash = window.location.hash

    if hash != '':
        hash = hash[1:]

        for panel in panels:
            if hash == panel:
                toggle_panel(hash)


collapse_in()
