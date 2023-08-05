#!/usr/bin/env python
# crate_anon/nlp_manager/lanuch_multiprocess_nlp.py

# Launch nlp_manager.py in multiprocess mode.
#
# Author: Rudolf Cardinal
# Copyright (C) 2015-2016 Rudolf Cardinal.
# License: http://www.apache.org/licenses/LICENSE-2.0
#
# Previous bash version:
#
# http://stackoverflow.com/questions/356100
# http://stackoverflow.com/questions/1644856
# http://stackoverflow.com/questions/8903239
# http://stackoverflow.com/questions/1951506
# Note: $! is the process ID of last process launched in background
# http://stackoverflow.com/questions/59895
#
# Python version:
#
# http://stackoverflow.com/questions/23611396/python-execute-cat-subprocess-in-parallel  # noqa
# http://stackoverflow.com/questions/320232/ensuring-subprocesses-are-dead-on-exiting-python-program  # noqa
# http://stackoverflow.com/questions/641420/how-should-i-log-while-using-multiprocessing-in-python  # noqa

import argparse
# import atexit
import logging
import multiprocessing
import sys
import time

from crate_anon.common.subproc import (
    check_call_process,
    run_multiple_processes,
)
from crate_anon.common.logsupport import configure_logger_for_colour
from crate_anon.nlp_manager.nlp_manager import NLP_CONFIG_ENV_VAR
from crate_anon.version import VERSION, VERSION_DATE

log = logging.getLogger(__name__)

NLP_MANAGER = 'crate_anon.nlp_manager.nlp_manager'

CPUCOUNT = multiprocessing.cpu_count()


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    version = "Version {} ({})".format(VERSION, VERSION_DATE)
    description = "Runs the CRATE NLP manager in parallel. {}.".format(version)
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("--config",
                        help="Config file (overriding environment "
                             "variable {})".format(NLP_CONFIG_ENV_VAR))
    parser.add_argument(
        "--nlpdef", "-a", required=True,
        help="NLP processing name, from the config file")

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-i", "--incremental", dest="incremental", action="store_true",
        help="Process only new/changed information, where possible "
             "(* default)")
    mode_group.add_argument(
        "-f", "--full", dest="incremental", action="store_false",
        help="Drop and remake everything")
    parser.set_defaults(incremental=True)

    parser.add_argument(
        "--nproc", "-n", nargs="?", type=int, default=CPUCOUNT,
        help="Number of processes (default: {})".format(CPUCOUNT))
    parser.add_argument(
        '--verbose', '-v', action='count', default=0,
        help="Be verbose (use twice for extra verbosity)")
    parser.add_argument(
        "--echo", action="store_true",
        help="Echo SQL")
    args = parser.parse_args()

    loglevel = logging.DEBUG if args.verbose > 0 else logging.INFO
    rootlogger = logging.getLogger()
    configure_logger_for_colour(rootlogger, loglevel)

    common_options = ['--nlpdef', args.nlpdef] + ["-v"] * args.verbose
    if args.config:
        common_options.extend(['--config', args.config])
    if args.echo:
        common_options.append('--echo')
    if args.incremental:
        common_options.append('--incremental')
    else:
        common_options.append('--full')

    log.debug("common_options: {}".format(common_options))

    nprocesses_main = args.nproc
    # nprocesses_index = args.nproc

    # -------------------------------------------------------------------------
    # Setup
    # -------------------------------------------------------------------------

    # Start.
    time_start = time.time()

    # -------------------------------------------------------------------------
    # Clean/build the tables. Only run one copy of this!
    # -------------------------------------------------------------------------
    # CALL USING "python -m my.module"; DO NOT run the script as an executable.
    # If you run a Python script as an executable, it gets added to the
    # PYTHONPATH. Then, when your script says "import regex" (meaning the
    # system module), it might import "regex.py" from the same directory (which
    # it wouldn't normally do, because Python 3 uses absolute not relative
    # imports).
    procargs = [
        sys.executable, '-m', NLP_MANAGER,
        '--dropremake',
        '--processcluster', 'STRUCTURE'
    ] + common_options
    check_call_process(procargs)

    # -------------------------------------------------------------------------
    # Now run lots of things simultaneously:
    # -------------------------------------------------------------------------
    # (a) patient tables
    args_list = []
    for procnum in range(nprocesses_main):
        procargs = [
            sys.executable, '-m', NLP_MANAGER,
            '--nlp',
            '--processcluster', 'NLP',
            '--nprocesses={}'.format(nprocesses_main),
            '--process={}'.format(procnum)
        ] + common_options
        args_list.append(procargs)
    run_multiple_processes(args_list)  # Wait for them all to finish

    # time_middle = time.time()

    # -------------------------------------------------------------------------
    # We used to index at the end.
    # (Always fastest to index last.)
    # But now we combine index definitions with column definitions in SQLA.
    # -------------------------------------------------------------------------
    # args_list = [
    #     [
    #         sys.executable, '-m', NLP_MANAGER,
    #         '--index',
    #         '--processcluster=INDEX',
    #         '--nprocesses={}'.format(nprocesses_index),
    #         '--process={}'.format(procnum)
    #     ] + common_options for procnum in range(nprocesses_index)
    # ]
    # run_multiple_processes(args_list)  # Wait for them all to finish

    # -------------------------------------------------------------------------
    # Finished.
    # -------------------------------------------------------------------------
    time_end = time.time()

    # main_dur = time_middle - time_start
    # index_dur = time_end - time_middle
    # total_dur = time_end - time_start
    # print("Time taken: main {} s, indexing {} s, total {} s".format(
    #     main_dur, index_dur, total_dur))

    total_dur = time_end - time_start
    print("Time taken: {} s".format(total_dur))


if __name__ == '__main__':
    main()
