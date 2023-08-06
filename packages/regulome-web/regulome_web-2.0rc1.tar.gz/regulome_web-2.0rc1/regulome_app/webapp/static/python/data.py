from browser import document, window, alert


panels = {
    'data_human_islet': (
        'data_pancreatic_islet_enhancers',
        'data_human_b_cell',
        'data_open_chromatin',
        'data_chromatin_state',
        'data_human_alpha_cell'
    ),
    'data_progenitor': (
        'data_invitro_progenitors',
    ),
    'data_gwas': (
        'data_diagram',
        'data_magic'
    )

}


def toggle_panel(hash):
    """Open and close the main panels"""
    for k, v in panels.items():
        if k == hash:
            document[k].class_name = 'panel-collapse collapse in'
            document[k + "_icon"].class_name = 'heading-basic-icon'
        else:
            document[k].class_name = 'panel-collapse collapse'
            document[k + "_icon"].class_name = 'heading-basic-icon collapsed'


def toggle_subpanel(hash):
    """Open and close the main panels"""
    for k, v in panels.items():
        for i in v:
            if i == hash:
                document[i].class_name = 'panel-collapse collapse in'
                document[i + "_icon"].class_name = 'heading-submit-options-icon'
                toggle_panel(k)
            else:
                document[i].class_name = 'panel-collapse collapse'
                document[i + "_icon"].class_name = 'heading-submit-options-icon collapsed'


def collapse_in():
    """Open a collapsed panel"""
    hash = window.location.hash

    if hash != '':
        hash = hash[1:]

        for key, values in panels.items():
            if hash == key:
                toggle_panel(hash)
            elif hash in values:
                toggle_subpanel(hash)


collapse_in()
