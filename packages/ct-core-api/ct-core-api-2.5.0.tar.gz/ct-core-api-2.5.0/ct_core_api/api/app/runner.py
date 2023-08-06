import optparse


def run(app, host='127.0.0.1', port='5000', debug=True, profile=False):
    """Run a local development server for a Flask app at the specified host and port,
    optionally in debug mode and with profiling enabled.
    """

    parser = optparse.OptionParser(
        description="Runs a local development server for the Flask application: '{}'".format(app.name))
    parser.add_option(
        '-H', '--host', default=host, help="Hostname of the Flask app [default {}]".format(host))
    parser.add_option(
        '-P', '--port', default=port, help="Port for the Flask app [default {}]".format(port))
    parser.add_option(
        '-d',
        '--debug',
        action='store_true',
        dest='debug',
        default=debug,
        help="Enable or disable debug mode [default {}]".format(debug))
    parser.add_option(
        '-p',
        '--profile',
        action='store_true',
        dest='profile',
        default=profile,
        help="Enable or disable the WSGI profiler middleware [default {}]".format(profile))

    options, _ = parser.parse_args()

    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
        options.debug = True

    app.run(debug=options.debug, host=options.host, port=int(options.port))
