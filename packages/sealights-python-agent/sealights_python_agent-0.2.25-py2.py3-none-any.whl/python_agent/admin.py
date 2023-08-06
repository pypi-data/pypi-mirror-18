import logging
import os
import sys
import json
from distutils.util import strtobool

from coverage.cmdline import Opts, unshell_list

import python_agent.utils
from python_agent.packages import click
from python_agent import config, init
from python_agent.build_scanner import main as build_scanner
from python_agent.test_listener.agent_manager import AgentManager
from python_agent.utils import validate_server, validate_server_api
if sys.version_info >= (2, 7):
    from python_agent.test_listener.integrations.unittest_helper import context_match, main as unittest_main
else:
    from python_agent.test_listener.integrations.unittest_26_helper import context_match, main as unittest_main

log = logging.getLogger(__name__)


@click.group()
@click.option("--customer_id", required=True, help="An id representing the client")
@click.option("--app_name", required=True, help="The name of the application")
@click.option("--server", type=validate_server, required=True,
              help="Sealights Server. Must be of the form: http[s]://<server>/api")
@click.option("--build", default=config.DEFAULT_BUILD, help="The build number of the application")
@click.option("--branch", default=config.DEFAULT_BRANCH, help="The branch of the current build")
@click.option("--labid", default=config.DEFAULT_ENV, help="The lab/machine name used for the current build")
@click.option("--proxy", type=validate_server_api,
              help="Go through proxy server. Must be of the form: http[s]://<server>")
@click.option(Opts.source.get_opt_string(), metavar=Opts.source.metavar, help=Opts.source.help, type=unshell_list)
@click.option(Opts.include.get_opt_string(), metavar=Opts.include.metavar, help=Opts.include.help, type=unshell_list)
@click.option(Opts.omit.get_opt_string(), metavar=Opts.omit.metavar, help=Opts.omit.help, type=unshell_list)
@click.pass_context
def cli(ctx, customer_id, app_name, server, build, branch, labid, proxy, source, include, omit):
    if ctx.invoked_subcommand == "run_program":
        return
    init.config_logging()
    args = {
        "customer_id": customer_id,
        "app_name": app_name,
        "server": server,
        "build": build,
        "branch": branch,
        "env": labid,
        "proxy": proxy,
        "source": source or [os.getcwd()],
        "include": include,
        "omit": omit
    }
    init.init_configuration(args)
    init.upgrade_agent()
    init.config_logging()
    AgentManager(**args)


@cli.command()
def build():
    build_scanner.main()


@cli.command(context_settings=dict(ignore_unknown_options=True,))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def unittest(args):
    config.CONTEXT_MATCH = context_match
    unittest_main(["unittest"] + list(args))


@cli.command(context_settings=dict(ignore_unknown_options=True,))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def unit2(args):
    config.CONTEXT_MATCH = context_match
    unittest_main(["unit2"] + list(args))


@cli.command(context_settings=dict(ignore_unknown_options=True,))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def pytest(args):
    try:
        args = list(args)
        from pytest import main as pytest_main
        from python_agent.test_listener.integrations import pytest_helper

        config.CONTEXT_MATCH = pytest_helper.context_match
        pytest_main(args=args, plugins=[pytest_helper.SealightsPlugin()])
    except ImportError as e:
        logging.exception("Failed Importing pytest. Error: %s" % str(e))


@cli.command(context_settings=dict(ignore_unknown_options=True,))
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def run_program(args):

    from python_agent import __file__ as root_directory

    root_directory = os.path.dirname(root_directory)
    boot_directory = os.path.join(root_directory, 'bootstrap')

    python_path = boot_directory

    if 'PYTHONPATH' in os.environ:
        path = os.environ['PYTHONPATH'].split(os.path.pathsep)
        if boot_directory not in path:
            python_path = "%s%s%s" % (boot_directory, os.path.pathsep, os.environ['PYTHONPATH'])

    os.environ['PYTHONPATH'] = python_path

    program_exe_path = args[0]

    if not os.path.dirname(program_exe_path):
        program_search_path = os.environ.get('PATH', '').split(os.path.pathsep)
        for path in program_search_path:
            path = os.path.join(path, program_exe_path)
            if os.path.exists(path) and os.access(path, os.X_OK):
                program_exe_path = path
                break

    run_program_index = sys.argv.index("run_program")

    with open(boot_directory + "/args.json", 'w') as f:
        prog_args = {"sl_args": sys.argv[1:run_program_index] + ["dummy_command"], "prog_name": program_exe_path}
        f.write("%s" % json.dumps(prog_args))

    os.execl(program_exe_path, *(list(args)))


@cli.command()
@click.option("--test_phase", metavar="Integration Tests,Functional Tests,...",
              help="A Flag Indicating This Build Is Multi Phase")
def start(test_phase):
    config.app["test_phase"] = test_phase
    python_agent.utils.start_execution()


@cli.command()
def end():
    python_agent.utils.end_execution()


@cli.command()
@click.option("--report_file", default=[], type=lambda f: f.split(","),
              help="The output report file path of the test execution result")
@click.option("--report_files_folder", default=[], type=lambda f: f.split(","),
              help="The output report folder path of the test execution results")
@click.option("--source", "unittest", help="The test framework used for running tests")
@click.option("--type", "JUnitReport", help="The type of test results report")
@click.option("--has_more_requests", default=True, type=strtobool,
              help="flag indicating if test results contains multiple reports. True for multiple reports. False otherwise")
def upload_report(report_file, report_files_folder, source, type, has_more_requests):
    if not report_file and not report_files_folder:
        log.error("At least one of --report_file, --report_files_folder must be provided")
    files = []
    files.extend(report_file)

    if files:
        for filename in os.listdir(report_files_folder):
            files.extend(filename)

        for file_path in files[:-1]:
            python_agent.utils.upload_report(file_path, source, type, True)

        python_agent.utils.upload_report(files[-1], source, type, has_more_requests)


@cli.command()
def dummy_command():
    pass


if __name__ == '__main__':
    cli()
