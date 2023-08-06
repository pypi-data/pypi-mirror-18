import os
import sys

from flask.cli import with_appcontext


########################################
# Shell Command (IPython)
########################################

def init_app(app):
    @app.cli.command('shell2', short_help='Runs an IPython shell in the app context.')
    @with_appcontext
    def shell_command():
        return run_ipython_shell()

    @app.shell_context_processor
    def shell_cmd_context():
        from ct_core_api.core.database import db
        return {'db': db}


def run_ipython_shell():
    """Runs an interactive IPython shell in the context of a given
    Flask application.  The application will populate the default
    namespace of this shell according to it's configuration.

    This is useful for executing small snippets of management code
    without having to manually configure the application.
    """
    import code
    from flask.globals import _app_ctx_stack
    current_app = _app_ctx_stack.top.app
    ctx = {}

    # Support the regular Python interpreter startup script if someone
    # is using it.
    startup = os.environ.get('PYTHONSTARTUP')
    if startup and os.path.isfile(startup):
        with open(startup, 'r') as f:
            eval(compile(f.read(), startup, 'exec'), ctx)

    ctx.update(current_app.make_shell_context())
    banner = 'Python %s on %s\nApp: %s%s\nInstance: %s\nContext: %s' % (
        sys.version,
        sys.platform,
        current_app.import_name,
        current_app.debug and ' [debug]' or '',
        current_app.instance_path,
        ', '.join(sorted(ctx.keys()))
    )

    # Try IPython
    try:
        try:
            # 0.10.x
            from IPython.Shell import IPShellEmbed
            ipshell = IPShellEmbed(banner=banner)
            ipshell(global_ns=dict(), local_ns=ctx)
        except ImportError:
            # 0.12+
            from IPython import embed
            embed(banner1=banner, user_ns=ctx)
        return
    except ImportError:
        pass

    code.interact(banner=banner, local=ctx)
