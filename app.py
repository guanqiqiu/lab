#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, g, redirect, render_template, request, url_for
from flask.ext.babel import Babel, get_locale

from settings import APP_URL, BABEL, CONTACT, MENUS, SERVER
from utils import read_csv_data, read_json_data, read_txt_data


app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = BABEL['default_locale']
app.debug = SERVER['debug']
app.jinja_env.globals.update(isinstance=isinstance, str=str)

babel = Babel(app, **BABEL)


@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')

@babel.localeselector
def get_locale():
    return g.get('current_lang', BABEL['default_locale'])


@app.route('/')
def root():
    return redirect(url_for('home', lang_code=BABEL['default_locale']))

@app.route('/<lang_code>/')
def home():
    return render_template('home.html')

@app.route('/<lang_code>/contact/')
def contact():
    return render_template('contact.html')

@app.route('/<lang_code>/courses')
def courses():
    return render_template('courses.html',
           courses=read_json_data('courses.json'))

@app.route('/<lang_code>/faq/')
def dummy_faq():
    return redirect(url_for('datamining'))

@app.route('/<lang_code>/faq/datamining')
def datamining():
    return render_template('datamining.html',\
           datamining=read_json_data('datamining.json'))

@app.route('/<lang_code>/faq/admission')
def admission():
    return render_template('admission.html',\
           admission=read_json_data('admission.json'))

@app.route('/<lang_code>/members')
def members():
    return render_template('members.html',\
           members=read_json_data('members.json'),
           alumni_phd=read_csv_data('alumni_phd.csv'),
           alumni_ms=read_csv_data('alumni_ms.tsv', sep='\t'))

@app.route('/projects/')
@app.route('/<lang_code>/projects/')
def projects():
    return redirect(url_for('faq'))

@app.route('/<lang_code>/projects/topics')
def topics():
    return render_template('topics.html',\
           topics=read_json_data('topics.json'))

@app.route('/<lang_code>/projects/faq')
def faq():
    print request.view_args
    return render_template('faq.html',\
           faq=read_json_data('faq.json'))

@app.route('/research/')
@app.route('/<lang_code>/research/')
def research():
    return redirect(url_for('publications'))

@app.route('/<lang_code>/research/methods')
def methods():
    return render_template('methods.html')

@app.route('/<lang_code>/research/publications')
def publications():
    return render_template('publications.html',\
           pub_dom_conferences=read_txt_data('pub_dom_conferences.txt'),
           pub_dom_journals=read_txt_data('pub_dom_journals.txt'),
           pub_int_conferences=read_txt_data('pub_int_conferences.txt'),
           pub_int_journals=read_txt_data('pub_int_journals.txt'),
           pub_patent =read_txt_data('pub_patent.txt'))

@app.route('/<lang_code>/software')
def software():
    return render_template('software.html',\
           software=read_json_data('software.json'))

@app.route('/~<name>')
def member(name):
    return redirect('%s/~%s' % (APP_URL, name))

@app.context_processor
def inject_vars():
    return dict(menus=MENUS, locale=get_locale(), contact=CONTACT)


if __name__=='__main__':
    app.run(SERVER['host'], SERVER['port'])
