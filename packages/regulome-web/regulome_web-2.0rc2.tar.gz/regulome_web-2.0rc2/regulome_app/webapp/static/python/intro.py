from browser import document, alert, ajax, html
import json
# import os  # This cannot be used because it takes too much time to load


# Global variables
URL = 'api'
CHROMOSOMES = [str(n) for n in range(1, 23)] + ['X', 'Y']
CHROMOSOME_LENGTHS = {
    "hg18": {
        'chromosome 1': 247249719,
        'chromosome 2': 242951149,
        'chromosome 3': 199501827,
        'chromosome 4': 191273063,
        'chromosome 5': 180857866,
        'chromosome 6': 170899992,
        'chromosome 7': 158821424,
        'chromosome 8': 146274826,
        'chromosome 9': 140273252,
        'chromosome 10': 135374737,
        'chromosome 11': 134452384,
        'chromosome 12': 132349534,
        'chromosome 13': 114142980,
        'chromosome 14': 106368585,
        'chromosome 15': 100338915,
        'chromosome 16': 88827254,
        'chromosome 17': 78774742,
        'chromosome 18': 76117153,
        'chromosome 19': 63811651,
        'chromosome 20': 62435964,
        'chromosome 21': 46944323,
        'chromosome 22': 49691432,
        'chromosome X': 154913754,
        'chromosome Y': 57772954,
        'chromosome M': 16571
    },
    "hg19": {
        'chromosome 1': 249250621,
        'chromosome 2': 243199373,
        'chromosome 3': 198022430,
        'chromosome 4': 191154276,
        'chromosome 5': 180915260,
        'chromosome 6': 171115067,
        'chromosome 7': 159138663,
        'chromosome 8': 146364022,
        'chromosome 9': 141213431,
        'chromosome 10': 135534747,
        'chromosome 11': 135006516,
        'chromosome 12': 133851895,
        'chromosome 13': 115169878,
        'chromosome 14': 107349540,
        'chromosome 15': 102531392,
        'chromosome 16': 90354753,
        'chromosome 17': 81195210,
        'chromosome 18': 78077248,
        'chromosome 19': 59128983,
        'chromosome 20': 63025520,
        'chromosome 21': 48129895,
        'chromosome 22': 51304566,
        'chromosome X': 155270560,
        'chromosome Y': 59373566,
        'chromosome M': 16571
    },
    "hg38": {
        'chromosome 1': 248956422,
        'chromosome 2': 242193529,
        'chromosome 3': 198295559,
        'chromosome 4': 190214555,
        'chromosome 5': 181538259,
        'chromosome 6': 170805979,
        'chromosome 7': 159345973,
        'chromosome 8': 145138636,
        'chromosome 9': 138394717,
        'chromosome 10': 133797422,
        'chromosome 11': 135086622,
        'chromosome 12': 133275309,
        'chromosome 13': 114364328,
        'chromosome 14': 107043718,
        'chromosome 15': 101991189,
        'chromosome 16': 90338345,
        'chromosome 17': 83257441,
        'chromosome 18': 80373285,
        'chromosome 19': 58617616,
        'chromosome 20': 64444167,
        'chromosome 21': 46709983,
        'chromosome 22': 50818468,
        'chromosome X': 156040895,
        'chromosome Y': 57227415,
        'chromosome M': 16569
    }
}
MIN_RANGE = 10
MAX_RANGE = 5000000


def on_complete(req):
    """Edits the elements of the form based in the ajax response"""
    if req.status in (0, 200):
        response = json.loads(req.text)
        # Inject the candidates on the datalist
        if response['fuzzy'] == 'True':
            options = ''
            for g in response['genes']:
                options += '<option value="{} ({}:{}-{})&nbsp;">'.format(g[0], g[1], g[2], g[3])
            document["gene_list"].html = options
        # Set the gene name
        else:
            g = response['genes'][0]
            rank = CHROMOSOMES.index(g[1][3:])
            document["gene_list"].html = ''
            document["gene_name"].value = "{} ({}:{}-{})".format(g[0], g[1], g[2], g[3])
            document["chromosome"].options[rank].selected = True
            document["start"].value = g[2]
            document["end"].value = g[3]
            document["chromosome_number"].value = g[1][3:]
    else:
        show_warning('Could not retrieve the gene details')
        # alert('ERROR: ' + req.text)


def get_gene_name(ev):
    """Gets the text written in the input field and send an ajax request"""
    build = document['build'].value
    gene_name = document["gene_name"].value
    if gene_name != '':
        if gene_name[-1] == chr(160):
            gene_name = gene_name[:-1].split()[0]
            # Query
            query = "build={}&gene_name={}&fuzzy=False".format(build, gene_name)
        else:
            # Query
            query = "build={}&gene_name={}&fuzzy=True".format(build, gene_name)
        req.open('GET', URL + '?' + query, True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send()


def change_build(ev):
    """Change the values of other fields according to the selected build"""
    gene_name = document["gene_name"].value
    # Reset the start and end coordinates to None
    document["start"].value = ''
    document["end"].value = ''

    if gene_name != '':
        document["gene_name"].value = gene_name.split()[0]
        get_gene_name(ev)


def create_plot(ev):
    """Submit the fhe form to create a plot"""
    if not check_submission():
        # Avoid to submit the form
        ev.preventDefault()
        ev.stopPropagation()


def check_submission():
    """Check that the data in the form are correct"""
    build = document['build'].value
    chromosome = document["chromosome"].value

    # If the coordinates are missing, it raises a warning
    if document['start'].value == '' or document['end'].value == '':
        show_warning("Start and/or end coordinates are missing")
        return False

    # Coordinates should be positive numbers
    try:
        start = int(document['start'].value)
    except ValueError as e:
        show_warning("Start position should be a positive integer")
        document['start'].focus()
        return False
    try:
        end = int(document['end'].value)
    except ValueError as e:
        show_warning("End position should be a positive integer")
        document['end'].focus()
        return False

    if start < 1:
        show_warning("Start position should be a positive integer")
        document['start'].focus()
        return False

    if end < 1:
        show_warning("End position should be a positive integer")
        document['end'].focus()
        return False

    # Start should be smaller than end
    if start >= end:
        show_warning("The 'start' coordinate should be smaller than the 'end' coordinate")
        document['start'].focus()
        return False

    # Check the chromosome length
    if end > CHROMOSOME_LENGTHS[build][chromosome]:
        show_warning('{} in {} is shorter than {}'.format(chromosome, build, end))
        document['end'].focus()
        return False

    # Check that the distance between start and end is > 10bp and < 5Mb
    if end - start < MIN_RANGE:
        show_warning('The plot should be at least 10bp')
        document['start'].focus()
        return False

    elif end - start > MAX_RANGE:
        show_warning('The plot should not exceed 5Mb')
        document['start'].focus()
        return False

    # TODO: If the gene name is not existing, it raises a warning
    return True


def show_warning(message):
    """Show a warning message in the contentmessages div"""
    document['message_div'].class_name = 'row messages_show'
    document['alert_message'].text = message


def hide_warning(ev=None):
    """Hide the warning messages"""
    if (ev is not None) or (ev is None and document['flash'].value == 'messages_hide'):
        document['alert_message'].text = ''
        document['message_div'].class_name = 'row messages_hide'


def choose_dataset(ev):
    """Load a dataset"""
    if ev.target.id == '_region_upload':
        document['region_file'].click()
    elif ev.target.id == '_snp_upload':
        document['snps_file'].click()


def notify_dataset(ev):
    """Write the name of the dataset on the input field"""
    file_path = ev.target.value
    if file_path != '':
        file_name = file_path.split('/')[-1] if '/' in file_path else file_path.split('\\')[-1]  # os.path.split(file_path)[1]
        if ev.target.id == 'region_file':
            document['reg_file_name'].value = file_name
        elif ev.target.id == 'snps_file':
            document['snps_file_name'].value = file_name


def upload_dataset(ev):
    """Trigger the submission to upload the dataset"""
    notify_dataset(ev)
    document['navbar_link'].value = 'upload'
    document['loader'].style.display = 'block'
    document['form_base'].action = 'submit'
    document['form_base'].submit()


def remove_uploaded_dataset(ev):
    """Remove the uploaded dataset from the messages"""
    if ev.target.id == 'clear_region_upload':
        document['reg_file_name'].value = ''
    elif ev.target.id == 'clear_snp_upload':
        document['snps_file_name'].value = ''
    document['navbar_link'].value = ev.target.id
    document['loader'].style.display = 'block'
    document['form_base'].action = 'submit'
    document['form_base'].submit()


# Events binding
document['gene_name'].bind('input', get_gene_name)
document['build'].bind('change', change_build)


# Button events binding
document['submit_button'].bind('click', create_plot)
document['message_div_button'].bind('click', hide_warning)
document['_region_upload'].bind('click', choose_dataset)
document['_snp_upload'].bind('click', choose_dataset)
document['region_file'].bind('change', upload_dataset)
document['snps_file'].bind('change', upload_dataset)
for _id in ('clear_region_upload', 'clear_snp_upload'):
    if _id in document:
        document[_id].bind('click', remove_uploaded_dataset)


# Ajax binding
req = ajax.ajax()
req.bind('complete', on_complete)
