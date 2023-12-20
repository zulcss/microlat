"""
Copyright (c) 2023 Wind River Systems, Inc.

SPDX-License-Identifier: Apache-2.0

"""

import pathlib

import click

from microlat.cmd import State

"""global options"""


def debug_option(f):
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.debug = value
        return value
    return click.option(
        "--debug",
        is_flag=True,
        help="Increase verbosity",
        callback=callback
    )(f)


def workspace_option(f):
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.workspace = pathlib.Path(value)
        return value
    return click.option(
        "--workspace",
        help="Path to the microlat workspace",
        nargs=1,
        default="/var/tmp/microlat",
        required=True,
        callback=callback
    )(f)

def config_option(f):
    def callback(ctxt, param, value):
        state = ctxt.ensure_object(State)
        state.config = pathlib.Path(value)
        return value
    return click.option(
        "--config",
        help="Path to configuration file",
        default="config/micorlat.yaml",
        nargs=1,
        callback=callback
    )(f)
