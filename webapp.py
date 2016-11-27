import os
import json
from subprocess import call
from tempfile import NamedTemporaryFile
from flask import Flask, request, render_template, url_for

from flask_wtf import Form
from wtforms import validators
from wtforms.fields.html5 import URLField
from flask_assets import Environment, Bundle


app = Flask(__name__)
assets = Environment(app)
css = Bundle(
    'css/custom.css',
    filters='cssmin', output='gen/all.css')
assets.register('css_all', css)
js = Bundle(
    'js/custom.js',
    filters='jsmin', output='gen/all.js')
assets.register('js_all', js)


class SearchForm(Form):
    address = URLField(
        validators=[validators.url()],
        render_kw={
            "placeholder":
            "https://www.leboncoin.fr/annonces/offres/..."})
    proxy = URLField(
        validators=[validators.Optional(), validators.url()],
        render_kw={"placeholder": "https://127.0.0.1:8080"})


def redirect_url(default='home'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def run_crawler(address, env=None):
    output_file = NamedTemporaryFile(delete=False, suffix=".json").name
    # output_file = "/tmp/data.json"
    scrapy_cmd = [
        'scrapy', 'crawl', 'leboncoin_car',
        '-a', 'start_urls=%s' % address,
        '-o', output_file]
    # cmdline.execute(scrapy_cmd)
    call(scrapy_cmd, env=env)
    data = json.load(open(output_file))
    os.unlink(output_file)
    return data


@app.route('/', methods=('GET', 'POST'))
def home():
    cars = []
    address = ''
    form = SearchForm(csrf_enabled=False)
    if form.validate_on_submit():
        address = form.address.data
        proxy_data = form.proxy.data
        env = None
        if proxy_data:
            env = dict(os.environ)
            env['HTTPS_PROXY'] = proxy_data
        cars = run_crawler(address, env)
        # adds price*KM
        for car in cars:
            if 'price' in car and 'mileage' in car:
                car['price_km'] = car['price'] * car['mileage']
    data = {
        "cars": cars,
        "form": form,
        "address": address,
    }
    return render_template('home.html', **data)


@app.route('/proxy')
def proxy():
    """
    Direct to template, proxy explained and list.
    """
    data = {}
    return render_template('proxy.html', **data)


# config app
if os.environ.get('PRODUCTION'):
    app.config.from_object('settings.ProductionSettings')
else:
    app.config.from_object('settings.DevelopmentSettings')
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(app.config['MAIL_SERVER'],
                               app.config['DEFAULT_FROM_EMAIL'],
                               app.config['ADMINS'],
                               app.config['EMAIL_SUBJECT_PREFIX'],
                               credentials=(
                                os.environ['SENDGRID_USERNAME'],
                                os.environ['SENDGRID_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
# useful for debugging in production
if os.environ.get('DEBUG'):
    app.debug = True
if __name__ == '__main__':
    app.run(port=8000)
