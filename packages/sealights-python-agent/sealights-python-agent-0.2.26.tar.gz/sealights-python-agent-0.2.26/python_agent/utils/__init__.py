import logging
import os
import argparse
import json
import subprocess
import urllib
from urlparse import urlparse
import functools
import time

import python_agent.packages.requests
from python_agent import config, VERSION
from python_agent.test_listener import utils


log = logging.getLogger(__name__)


def retries(logger, tries=3, quiet=True):
    def inner(f):
        @functools.wraps(f)
        def inner_args(*args, **kwargs):
            for i in range(tries):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logger.warn("failed try #%s running function %s. args: %s exception: %s"
                                % (str(i + 1), f.func_name, str(args), unicode(e)),  exc_info=True)
                    time.sleep(2 * i)
            if quiet:
                return
            raise
        return inner_args
    return inner


def exception_handler(log, quiet=True, message=None):
    def f_exception_handler(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.exception("%s. Error: %s. Args: %s. Kwargs: %s" % (message, str(e), args, kwargs))
                if not quiet:
                    raise
        return wrapper
    return f_exception_handler


def get_top_relative_path(filepath):
    return os.path.relpath(filepath, os.getcwd())


def validate_server_api(server, is_validate_api=False):
    error_msg = "Must be of the form: http[s]://<server>/api"
    try:
        result = urlparse(server)
        if result.scheme not in ["http", "https"]:
            raise argparse.ArgumentTypeError(error_msg)
        if is_validate_api and "/api" not in result.path:
            raise argparse.ArgumentTypeError(error_msg)
    except Exception:
        raise argparse.ArgumentTypeError(error_msg)
    return server


def validate_server(server):
    return validate_server_api(server, is_validate_api=True)


def get_config_from_server(server, customer_id, app_name, branch, env):
    server_config = {}
    url = None
    try:
        params = ["v1", "config", customer_id, "null", app_name, branch, env, config.app["technology"], VERSION]
        params = [server] + [urllib.quote(param, safe=":") for param in params]
        url = "/".join(params)
        response = python_agent.packages.requests.get(url)
        config_data = response.json()
        config_data = config_data.get("config", "{}")
        server_config = json.loads(config_data)
        response.raise_for_status()
        log.info("Fetched Configuration From Server. Configuration: %s" % server_config)
    except Exception as e:
        log.warning("Failed Fetching Configuration From Server. URL: %s. Error: %s" % (url, str(e)))
    return server_config


def get_repo_url():
    raw_url = ""
    try:
        raw_url = subprocess.Popen(['git', 'config', '--get', 'remote.origin.url'], stdout=subprocess.PIPE).communicate()[0].replace("\n", "")
    except Exception as e:
        log.warning("Failed Getting Repo URL. Error: %s" % str(e))
    return raw_url


def get_commit_history():
    commits = []
    try:
        commits = subprocess.Popen(['git', 'log', '--format=%H', '-n', '100'], stdout=subprocess.PIPE).communicate()[0].split("\n")
        commits = commits[:-1]
    except Exception as e:
        log.warning("Failed Getting Commit History. Error: %s" % str(e))
    return commits


@retries(log)
def start_execution():
    data = {
        "customerId": config.app.get("customer_id"),
        "appName": config.app.get("app_name"),
        "newEnvironment": config.app.get("test_phase")
    }
    if config.app.get("env"):
        data["environment"] = config.app.get("env")

    if config.app.get("build"):
        data["buildName"] = config.app.get("build")

    if config.app.get("branch"):
        data["branchName"] = config.app.get("branch")

    url = config.app["server"] + config.TEST_EXECUTION_ROUTE
    log.info("Sending Start Execution. URL: %s. Data: %s" % (url, data))
    response = python_agent.packages.requests.post(url, json=data, verify=False)
    response.raise_for_status()
    log.info("Sent Start Execution. Response: %s" % response.content)


@retries(log)
def end_execution():
    params = {
        "customerId": config.app.get("customer_id"),
        "appName": config.app.get("app_name"),
    }
    if config.app.get("env"):
        params["environment"] = config.app.get("env")

    if config.app.get("build"):
        params["buildName"] = config.app.get("build")

    if config.app.get("branch"):
        params["branchName"] = config.app.get("branch")

    url = config.app["server"] + config.TEST_EXECUTION_ROUTE
    log.info("Sending End Execution. URL: %s. Params: %s" % (url, params))
    response = python_agent.packages.requests.delete(url, params=params, verify=False)
    response.raise_for_status()
    log.info("Sent End Execution. Response: %s" % response.content)


@retries(log)
def upload_report(report_path, source, type, has_more_requests):
    metadata_path = os.path.dirname(__file__) + "/metadata.json"
    if not os.path.isfile(report_path):
        log.exception("XML Report Doesn't Exist. Path Checked: %s" % report_path)
        return
    with open(metadata_path, 'w') as f:
        f.write(json.dumps({
            "source": source,
            "type": type,
            "customerId": config.app["customer_id"],
            "appName": config.app["app_name"],
            "environment": utils.create_environment(),
            "hasMoreRequests": has_more_requests
        }))
    data = (("metadata", open(metadata_path, "r")), ("report", open(report_path, "r")))
    url = config.app["server"] + config.EXTERNAL_DATA_ROUTE

    log.info("Uploading JUnit Report. URL: %s." % url)
    response = python_agent.packages.requests.post(url, files=data, verify=False)
    response.raise_for_status()
    log.info("Uploaded Report. URL: %s. Report Path: %s" % (url, report_path))
