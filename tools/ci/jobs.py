import argparse
import os
import re
from ..wpt.testfiles import branch_point, files_changed, affected_testfiles

wpt_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

# Rules are just regex on the path, with a leading ! indicating a regex that must not
# match for the job
job_path_map = {
    "testharness_unittest": ["resources/"],
    "stability": [".*/.*",
                  "!tools/",
                  "!docs/",
                  "!resources/*",
                  "!conformance-checkers/",
                  "!.*/OWNERS",
                  "!.*/tools/",
                  "!.*/README",
                  "!css/[^/]*$"],
    "lint": [".*"],
    "tools_unittest": ["tools/"],
    "wptrunner_unittest": ["tools/wptrunner/*"],
    "build_css": ["css/"],
    "update_built": ["2dcontext/",
                     "assumptions/",
                     "html/",
                     "offscreen-canvas/"],
    "wpt_integration": ["tools/"],
}


class Ruleset(object):
    def __init__(self, rules):
        self.include = []
        self.exclude = []
        for rule in rules:
            self.add_rule(rule)

    def add_rule(self, rule):
        if rule.startswith("!"):
            target = self.exclude
            rule = rule[1:]
        else:
            target = self.include

        target.append(re.compile("^%s" % rule))

    def __call__(self, path):
        if os.path.sep != "/":
            path = path.replace(os.path.sep, "/")
        path = os.path.normcase(path)
        for item in self.exclude:
            if item.match(path):
                return False
        for item in self.include:
            if item.match(path):
                return True
        return False

    def __repr__(self):
        subs = tuple(",".join(item.pattern for item in target)
                     for target in (self.include, self.exclude))
        return "Rules<include:[%s] exclude:[%s]>" % subs


def get_paths(**kwargs):
    if kwargs["revish"] is None:
        revish = "%s..HEAD" % branch_point()
    else:
        revish = kwargs["revish"]

    changed, _ = files_changed(revish)
    all_changed = set(os.path.relpath(item, wpt_root)
                      for item in set(changed))
    return all_changed


def get_jobs(paths, **kwargs):
    jobs = set()

    rules = {}
    includes = kwargs.get("includes")
    if includes is not None:
        includes = set(includes)
    for key, value in job_path_map.iteritems():
        if includes is None or key in includes:
            rules[key] = Ruleset(value)

    for path in paths:
        for job in rules.keys():
            ruleset = rules[job]
            if ruleset(path):
                rules.pop(job)
                jobs.add(job)
        if not rules:
            break

    return jobs


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("revish", default=None, help="Commits to consider. Defaults to the commits on the current branch", nargs="?")
    parser.add_argument("--includes", default=None, help="Jobs to check for. Return code is 0 if all jobs are found, otherwise 1", nargs="*")
    return parser


def run(**kwargs):
    paths = get_paths(**kwargs)
    jobs = get_jobs(paths, **kwargs)
    if not kwargs["includes"]:
        for item in sorted(jobs):
            print(item)
    else:
        return 0 if set(kwargs["includes"]) == jobs else 1
