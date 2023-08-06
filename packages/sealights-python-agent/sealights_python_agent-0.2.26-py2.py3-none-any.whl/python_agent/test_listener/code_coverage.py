import logging
import re
from copy import deepcopy

try:
    from coverage import Coverage
except ImportError:
    from coverage import coverage as Coverage

from python_agent.build_scanner import file_signature
from python_agent.packages.intervaltree import IntervalTree
from python_agent.utils import get_top_relative_path
from python_agent.packages.deepdiff import DeepDiff

log = logging.getLogger(__name__)


class CodeCoverageManager(object):

    def __init__(self, source=None, include=None, omit=None, branch=None, **kwargs):
        self.files_signatures = {}
        self.past_coverage = {}
        self.coverage = Coverage(source=source, include=include, omit=omit)
        self.coverage.start()
        log.info("Started Code Coverage Manager")

    def get_coverage_delta(self, test_name):
        test_coverage = {}
        current_coverage = self.coverage.collector.data
        if not current_coverage:
            log.info("No Coverage Found")
            return {}

        deep_diff = DeepDiff(self.past_coverage, current_coverage, ignore_order=True, verbose_level=2)
        added = deep_diff.get("dictionary_item_added")
        if added:
            for added_key, added_value in added.items():
                added_key = added_key[4:].replace("\'", "")  # remove "root"
                keys = re.findall(r'\[([^]]*)\]', added_key)
                if len(keys) == 1:  # new file
                    test_coverage[keys[0]] = added_value
                if len(keys) == 2:  # new line in file
                    if test_coverage.has_key(keys[0]):
                        test_coverage[keys[0]].update({keys[1]: added_value})
                    else:
                        test_coverage[keys[0]] = {keys[1]: added_value}

        self.past_coverage = deepcopy(current_coverage)
        return test_coverage

    def get_coverage(self, test_name):
        self.coverage.stop()
        test_coverage = self.coverage.collector.data
        if not test_coverage:
            log.info("No Coverage Found")

        log.info("Resetting Coverage After Fetching Footprints For Test: %s" % test_name)
        self.reset_coverage()
        log.info("Coverage Reset For Test: %s" % test_name)
        self.coverage.start()
        log.info("Coverage Started After Test: %s" % test_name)

        return test_coverage

    def get_footprints_from_test(self, test_coverage, test_name):
        footprints = []

        for filename, covered_lines in test_coverage.items():
            file_sig = self.files_signatures.get(filename)
            if not file_sig:
                file_sig = file_signature.calculate_file_signature(filename, get_top_relative_path(filename))
                # file_range_tree = self.create_range_tree(file_sig)
                self.files_signatures[filename] = file_sig
            # covered_methods = self._new_lines_to_methods(file_range_tree, covered_lines)
            covered_methods = self._lines_to_methods(file_sig.get("methods", []), covered_lines, test_name)
            file_footprints = map(lambda method: {"name": method["uniqueName"], "hash": method["hash"], "hits": 1},
                                  covered_methods)
            log.debug("Found Coverage For Test: %s. Number Of Methods: %s" % (test_name, len(file_footprints)))
            footprints.extend(file_footprints)

        return footprints

    def _lines_to_methods(self, methods, covered_lines, test_name):
        line_methods = {}
        sorted_methods = sorted(methods, key=lambda method: method.get("position")[0], reverse=True)
        for method in sorted_methods:
            for line_num in covered_lines.keys():
                if self._is_match(method, int(line_num)):
                    line_methods[method["uniqueName"]] = method
                    log.debug("Found Coverage For Method: %s. Test: %s" % (method, test_name))
                    break
        return line_methods.values()

    def _new_lines_to_methods(self, range_tree, covered_lines):
        covered_methods = {}
        for line_num in covered_lines.keys():
            intervals = list(range_tree.search(line_num))
            if not intervals:
                continue
            if len(intervals) > 1:
                intervals = sorted(intervals, reverse=True)
            interval = intervals[0]
            covered_methods["uniqueName"] = interval.data
        return covered_methods.values()

    def _is_match(self, method, line_num):
        """
        In python, on file import, the python interpreter scans the file and goes over method definitions.
         That means, that all method definition lines get hit from the coverage.py perspective,
         even though, this method might not be called.

         Sadly, there are methods that their definition and body is on the same line.
         example:
            (1) def foo(a, b): return a + b
            (2) lambda x: x + 1
        These kind of methods we count as a hit anyway. We do that since the coverage.py tool does that too.
        :param method: the candidate method to match against the line number
        :param line_num: the line number that was hit
        :return: True if we have a match, False otherwise
        """

        # default method definition. We don't include the first line
        is_match = method["position"][0] < line_num <= method["endPosition"][0]

        # one liner method. We include the first line
        if method["position"][0] == method["endPosition"][0]:
            is_match = method["position"][0] <= line_num <= method["endPosition"][0]

        return is_match

    def create_range_tree(self, file_sig):
        methods = file_sig["methods"] or []
        tree = IntervalTree()
        for method in methods:
            tree[method["position"][0]:method["endPosition"][0] + 1] = method
        return tree

    def shutdown(self):
        self.coverage.stop()
        self.coverage.save()
        log.info("Finished Shutting Down Code Coverage Manager")

    def reset_coverage(self):
        self.coverage.collector.data = {}
