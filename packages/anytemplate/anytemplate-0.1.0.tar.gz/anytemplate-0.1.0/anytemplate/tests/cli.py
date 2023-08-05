#
# Copyright (C) 2015 Satoru SATOH <ssato at redhat.com>
# License: MIT
#
# pylint: disable=missing-docstring
"""Tests of anytempalte.cli
"""
import os.path
import os
import unittest

import anytemplate.cli as TT
import anytemplate.tests.common

from anytemplate.engine import find_by_name


CLI_SCRIPT = os.path.join(anytemplate.tests.common.selfdir(), "..", "cli.py")


def run_and_check_exit_code(args=None, code=0):
    """
    Run main() and check its exit code.
    """
    try:
        TT.main(["dummy"] + ([] if args is None else args))
    except SystemExit as exc:
        return exc.code == code

    return True


class Test00(unittest.TestCase):

    def run_and_check_exit_code(self, args=None, code=0, _not=False):
        if args is None:
            args = []
        if _not:
            self.assertFalse(run_and_check_exit_code(args, code))
        else:
            self.assertTrue(run_and_check_exit_code(args, code))

    def test_10_main__wo_args(self):
        self.run_and_check_exit_code()

    def test_12__show_usage(self):
        self.run_and_check_exit_code(["--help"])

    def test_14__wrong_option(self):
        self.run_and_check_exit_code(["--wrong-option-xyz"], _not=True)

    def test_20_main__wo_args(self):
        self.assertRaises(SystemExit, TT.main, [])

    def test_22_main__show_usage(self):
        self.assertRaises(SystemExit, TT.main, ["dummy", "--help"])

    def test_24_main__show_usage(self):
        self.assertRaises(SystemExit, TT.main, ["dummy", "--wrong-option"])

    def test_26_main__list_engines(self):
        TT.main(["dummy", "--list-engines"])


class Test10(anytemplate.tests.common.TestsWithWorkdir):

    def run_and_check_exit_code(self, args=None, code=0, _not=False):
        if args is None:
            args = []
        if _not:
            self.assertFalse(run_and_check_exit_code(args, code))
        else:
            self.assertTrue(run_and_check_exit_code(args, code))

    def test_10_main__strtemplate(self):
        tmpl = os.path.join(self.workdir, "test.tmpl")
        ctx = os.path.join(self.workdir, "ctx.yml")
        output = os.path.join(self.workdir, "output.txt")
        open(tmpl, 'w').write("$a\n")
        open(ctx, 'w').write("a: aaa\n")

        self.run_and_check_exit_code(["-E", "string.Template", "-C", ctx,
                                      "-o", output, tmpl])
        self.assertEquals(open(output).read(), "aaa\n")

    def test_20_main__jinja2(self):
        if find_by_name("jinja2"):
            tmpl = os.path.join(self.workdir, "test.j2")
            output = os.path.join(self.workdir, "output.txt")
            open(tmpl, 'w').write("{{ hello|default('hello') }}")

            self.run_and_check_exit_code(["-o", output, tmpl])
            self.assertEquals(open(output).read(), "hello")

# vim:sw=4:ts=4:et:
