# Import modules
import json
import os
import sqlite3
from regulome_app.webapp.app import app  # , db
from regulome_app.config import logger, configs
from regulome_app.webapp import models as models
from flask import render_template, url_for, redirect, flash, session, request, send_from_directory, jsonify
from collections import defaultdict
from regulome_app.webapp.tools.parse_messages import ParseMessage
from regulome_app.webapp.tools.plot import Plot
from regulome_app.webapp.tools.uploads import Upload
from werkzeug.utils import secure_filename


# Global variables
__author__ = 'Loris Mularoni'

genes_coords = {}
for build in models.BUILDS.keys():
    file_path = os.path.join(configs['data']['data'], build, '{}_UCSC_RefSeq_genes_simple.txt'.format(build))
    genes_coords[build] = defaultdict(list)
    with open(file_path, 'r') as fi:
        for line in fi:
            line = line.strip().split('\t')
            gene, chromosome, strand, start, end, _ = line
            gene = gene.upper()
            genes_coords[build][gene].append((gene, chromosome, start, end))


@app.context_processor
def inject_globals():
    deploy_mode = configs['deploy_mode']['configuration']
    return dict(
        deploy_mode=deploy_mode if deploy_mode in ('development', 'testing', 'production') else 'development',
        snps=models.SNPS,
        builds=models.BUILDS,
        chromosomes=models.CHROMOSOMES_SORTED,
        regions=models.REGIONS,
        tfbs=models.TFBS,
        chromatin=models.CHROMATIN,
        ranges=models.RANGES
    )


def reset_session_messages():
    """Reset the session messages to the default values"""
    session['messages'] = json.dumps(models.default_messages)


def update_messages(new_messages):
    """Update the information of messages"""
    messages = json.loads(session['messages'])
    for key, value in new_messages.items():
        messages[key] = value
    session['messages'] = json.dumps(messages)


@app.route('/')
def root():
    return redirect(url_for('intro'))


@app.route('/home', methods=['GET', 'POST'])
def intro():
    """Show the intro page or redirect to another page"""
    if 'username' not in session:
        session['username'] = os.urandom(24).hex()
    if 'messages' not in session:
        reset_session_messages()
    if request.form.get('action', None) == 'submit':
        messages = ParseMessage(messages=json.dumps(request.form))
        session['messages'] = messages.get_json()
        return redirect(url_for('visualize_plot'))
    elif request.form.get('action', None) == 'upload':
        update_messages(request.form)
        # The argument code is to force a POST redirect
        return redirect(url_for('upload_file'), code=307)
    else:
        # Restore the previous options
        return render_template('intro.html', messages=json.loads(session['messages']))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Parse the submission of the form"""
    if request.form.get('navbar_link', None) in ('home', 'home_main'):
        return redirect(url_for('intro'))
    elif request.form.get('navbar_link', None) == 'data':
        return redirect(url_for('data'))
    elif request.form.get('navbar_link', None) == 'credits':
        return redirect(url_for('credits'))
    elif request.form.get('navbar_link', None) == 'contact':
        return redirect(url_for('contact'))
    elif request.form.get('navbar_link', None) == 'info':
        return redirect(url_for('info'))
    elif request.form.get('navbar_link', None) == 'upload':
        update_messages(request.form)
        # The argument code is to force a POST redirect
        return redirect(url_for('upload_file'), code=307)
    elif request.form.get('navbar_link', None) in ('clear_region_upload', 'clear_snp_upload'):
        messages = json.loads(session['messages'])
        if request.form.get('navbar_link') == 'clear_region_upload':
            messages['upload_regions'] = 'None'
        else:
            messages['upload_snps'] = 'None'
        session['messages'] = json.dumps(messages)
        return redirect(url_for('intro'))
    else:
        try:
            messages = ParseMessage(messages=json.dumps(request.form))
            session['messages'] = messages.get_json()
            return redirect(url_for('visualize_plot'))
        except KeyError as e:
            return redirect(url_for('intro'))


@app.route('/show')
def visualize_plot(messages=None):
    """Create and visualize the plot"""
    if messages is None:
        # Redirect to the home page
        if 'messages' not in session:
            return redirect(url_for('intro'))

        messages = json.loads(session['messages'])
        plot = Plot(messages=messages, username=session['username'])
        plot.run()
        messages['file_path'] = plot.get_results_path()
        messages['file_name'] = plot.get_results_name()
        messages['downloads'] = enable_downloads(messages['file_path'])
        messages['table'] = table(messages['file_path'], messages['region'])

    return render_template('plot.html', messages=messages)


@app.route('/cache/<path:filename>')
def cache(filename):
    """Return the path of a file in the cache folder"""
    return send_from_directory(configs['output']['cache'], filename, as_attachment=True)


@app.route('/api', methods=['GET'])
def retrieve_genes():
    """Retrieve the genes matching the gene_name"""
    build = request.args.get('build', None)
    gene_name = request.args.get('gene_name', None)
    fuzzy = eval(request.args.get('fuzzy', None))

    # sql_file = os.path.join(configs['data']['data'], build, '{}_genes.db'.format(build))
    # genes = query_sql(sql_file, gene_name)
    # genes = [gene for gene in genes if gene[6] == 'gene']
    # gene_file = os.path.join(configs['data']['data'], build, '{}_UCSC_RefSeq_genes_simple.txt'.format(build))
    # genes = query_file(gene_file, gene_name, fuzzy)
    if fuzzy:
        genes = []
        for gene in genes_coords[build].keys():
            if gene.startswith(gene_name.upper()):
                for isoform in genes_coords[build][gene]:
                    genes.append(isoform)
        genes = sorted(genes)[:6]
    else:
        genes = genes_coords[build][gene_name] if gene_name in genes_coords[build].keys() else []
    return jsonify({'genes': genes, 'fuzzy': fuzzy})


def query_file(file_path, symbol, fuzzy):
    """Return up to 10 lines of the file where the
    initials of the gene correspond to symbol.
    """
    genes = []
    with open(file_path, 'r') as fi:
        for line in fi:
            line = line.strip().split('\t')
            gene, chromosome, strand, start, end, _ = line
            gene = gene.upper()
            if fuzzy and gene.startswith(symbol.upper()):
                genes.append((gene, chromosome, start, end))
            elif not fuzzy and gene == symbol.upper():
                return gene.upper(), chromosome, start, end
    return genes[:10]


def query_sql(db, symbol):
    """Queries a sqlite database. Return up to
    10 genes whose initials correspond to symbol
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    query = "SELECT * FROM {} WHERE SYMBOL LIKE '{}%' LIMIT 10;".format('genes', symbol)
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result


@app.route('/credits')
def credits():
    """Show the credit page"""
    return render_template('credits.html')


@app.route('/contact')
def contact():
    """Show the contact page"""
    return render_template('contact.html')


@app.route('/info')
def info():
    """Show the info page"""
    return render_template('info.html')


@app.route('/data')
def data():
    """Show the data page"""
    return render_template('data.html')


@app.route('/show/<key>')
def get_message(key):
    return render_template('intro.html',
                           message=models.MESSAGES.get(key) or "{} not found!".format(key))


@app.route('/add/<key>/<message>')
def add_or_update_message(key, message):
    models.MESSAGES[key] = message
    return render_template('intro.html', message="{} Added/Updated".format(key))


def enable_downloads(file_path):
    """Calculates which files could be downloaded"""
    downloads = {}
    for name, extensions in zip(('sites', 'snps', 'figures'),
                                (['.txt'], ['.snp.txt'], ['.png', '.pdf'])):
        if all([os.path.exists(os.path.join(configs['output']['cache'], file_path + extension))
                for extension in extensions]):
            downloads[name] = ''
        else:
            downloads[name] = 'disabled'
    return downloads


@app.route('/downloads', methods=['POST'])
def downloads():
    """Return the path of a file in the cache folder"""
    if request.form.get('download', None) == 'download_table':
        filepath = request.form.get('file_path') + '.txt'
        filename = request.form.get('file_name') + '.txt'
        return send_from_directory(
            configs['output']['cache'],
            filepath,
            attachment_filename=filename,
            as_attachment=True
        )
    elif request.form.get('download', None) == 'download_snps':
        filepath = request.form.get('file_path') + '.snp.txt'
        filename = request.form.get('file_name') + '.snp.txt'
        return send_from_directory(
            configs['output']['cache'],
            filepath,
            attachment_filename=filename,
            as_attachment=True
        )
    elif request.form.get('download', None) == 'download_pdf':
        filepath = request.form.get('file_path') + '.pdf'
        filename = request.form.get('file_name') + '.pdf'

        return send_from_directory(
            configs['output']['cache'],
            filepath,
            attachment_filename=filename,
            as_attachment=True
        )
    elif request.form.get('download', None) == 'download_png':
        filepath = request.form.get('file_path') + '.png'
        filename = request.form.get('file_name') + '.png'
        return send_from_directory(
            configs['output']['cache'],
            filepath,
            attachment_filename=filename,
            as_attachment=True
        )
    else:
        flash('An error occurred.')
        return render_template('plot.html', messages=request.form)


def table(file_path, region):
    """Return the elements of an html table"""
    filename = os.path.join(configs['output']['cache'], file_path + '.txt')
    table = []

    try:
        tfs = None
        with open(filename, 'r') as fi:
            for i, line in enumerate(fi):
                # Skip the header
                if i == 0:
                    continue
                if region == 'adult':
                    chromosome, start, end, group, tfs, _ = line.split("\t")
                elif region == 'adultStretch':
                    chromosome, start, end, group, _ = line.split("\t")
                elif region == 'progenitor':
                    chromosome, start, group, end, _ = line.split("\t")

                color = models.COLORS[region][group]
                font_color = "white" if color == (0, 0, 0) else "black"
                table.append(dict())
                table[-1]['color'] = color
                table[-1]['font_color'] = font_color
                table[-1]['group'] = group
                table[-1]['chromosome'] = models.CHROMOSOMES_DICT_R[chromosome]
                table[-1]['start'] = start
                table[-1]['end'] = end

                if tfs is not None:
                    table[-1]['tfs'] = tfs

    except FileNotFoundError as e:
        with open(configs['logs']['regulome_log'], 'a') as log:
            log.write("FileNotFoundError in table: {}".format(filename))
    except Exception as e:
        with open(configs['logs']['regulome_log'], 'a') as log:
            log.write("Exception in table: {}".format(filename))
            log.write("Exception is: {}".format(e))
    finally:
        return table


@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    """Save an uploaded file"""
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'region_file' not in request.files and 'snps_file' not in request.files:  # regions_upload, snp_upload
            return redirect(request.url)
        elif request.files['region_file'] == '' and request.files['snps_file'] == '':
            flash('Please select a file to download')
            return redirect(request.url)
        for upload_tag, upload_id in zip(
                ('region_file', 'snps_file'),
                ('upload_regions', 'upload_snps')):
            f = request.files[upload_tag]

            # If the user does not select any file, browser also
            # submits an empty part without filename
            if f.filename == '':
                continue
            if f:  # and allowed_file(file.filename):
                filename = secure_filename(f.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                        "{}_{}".format(session['username'], filename))
                f.save(filepath + '.raw')

                # Verify the validity of the uploaded file
                upload = Upload(input_file=filepath + '.raw',
                                type_of_file=upload_tag,
                                output_file=filepath)
                if upload.get_errors():
                    flash(upload.get_errors())
                    return redirect(url_for('intro'))
                else:
                    messages = json.loads(session['messages'])
                    messages[upload_id] = filename
                    session['messages'] = json.dumps(messages)
    return redirect(url_for('intro'))


# class Regions(db.Model):
#     __bind_key__ = 'regions'
#     id = db.Column(db.Integer, primary_key=True)
#     # username = db.Columns(db.String(80), unique=True)


