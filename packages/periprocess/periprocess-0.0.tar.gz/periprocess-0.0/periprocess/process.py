#!/usr/bin/env python

"""
multiprocessing/subprocess front-end
"""

# imports
import argparse
import atexit
import os
import signal
import subprocess # http://bugs.python.org/issue1731717
import sys
import time
import tempfile


# globals
__all__ = ['Process']
string = (str, unicode)
PIDS = set()

# ensure subprocesses gets killed on exit
def killall():
    """kill all subprocess PIDs"""
    global PIDS
    for pid in PIDS.copy():
        try:
            os.kill(pid, 9) # SIGKILL
            PIDS.discard(pid)
        except:
            sys.stderr.write("Unable to kill PID {}\n".format(pid))
atexit.register(killall)


signals = (signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGSEGV, signal.SIGTERM) # signals to handle
fatal = set([signal.SIGINT, signal.SIGSEGV, signal.SIGKILL, signal.SIGTERM])
# ensure subprocesses get killed on signals
def sighandler(signum, frame):
    """https://docs.python.org/2/library/signal.html"""
    sys.stderr.write('Signal handler called with signal {}\n; terminating subprocesses: {}'.format(signum,
                                                                                                   ', '.join([str(pid) for pid in sorted(PIDS)])))
    killall()
    if signum in fatal:
        print ("Caught signal {}; exiting".format(signum))
        sys.exit()
for signum in signals:
    try:
        signal.signal(signum, sighandler)
    except RuntimeError as e:
        print ('[{}] {}'.format(signum, e))
        raise

class Process(subprocess.Popen):
    """why would you name a subprocess object Popen?"""

    # http://docs.python.org/2/library/subprocess.html#popen-constructor
    defaults = {'bufsize': 1, # line buffered
                'store_output': True, # store stdout
                }

    def __init__(self, command, **kwargs):

        # get verbosity
        self.verbose = kwargs.pop('verbose', False)

        # setup arguments
        self.command = command
        _kwargs = self.defaults.copy()
        _kwargs.update(kwargs)


        # on unix, ``shell={True|False}`` should always come from the
        # type of command (string or list)
        if not subprocess.mswindows:
            _kwargs['shell'] = isinstance(command, string)

        # output buffer
        self.location = 0
        self.output_buffer = tempfile.SpooledTemporaryFile()
        self.output = '' if _kwargs.pop('store_output') else None
        _kwargs['stdout'] = self.output_buffer

        # ensure child in process group
        # see :
        # - http://pymotw.com/2/subprocess/#process-groups-sessions
        # - http://ptspts.blogspot.com/2012/11/how-to-start-and-kill-unix-process-tree.html
        _kwargs['preexec_fn'] = os.setpgrp

        # runtime
        self.start = time.time()
        self.end = None

        if self.verbose:
            # print useful info
            print ("Running `{}`; started: {}".format(str(self), self.start))

        # launch subprocess
        try:
            subprocess.Popen.__init__(self, command, **_kwargs)
            PIDS.add(self.pid)
            if self.verbose:
                # print the PID
                print ("PID: {}".format(self.pid))
        except:
            # print the command
            print ("Failure to run:")
            print (self.command)

            # reraise the hard way:
            # http://www.ianbicking.org/blog/2007/09/re-raising-exceptions.html
            exc = sys.exc_info()
            raise exc[0], exc[1], exc[2]


    def _finalize(self, process_output):
        """internal function to finalize"""

        # read final output
        if process_output is not None:
            self.read(process_output)

        # reset output buffer location
        self.output_buffer.seek(0)

        # set end time
        self.end = time.time()

        # remove PID from list
        PIDS.discard(self.pid)

    def poll(self, process_output=None):

        if process_output is not None:
            self.read(process_output) # read from output buffer
        poll = subprocess.Popen.poll(self)
        if poll is not None:
            self._finalize(process_output)
        return poll

    def wait(self, maxtime=None, sleep=1., process_output=None):
        """
        maxtime -- timeout in seconds
        sleep -- number of seconds to sleep between polling
        """
        while self.poll(process_output) is None:

            # check for timeout
            curr_time = time.time()
            run_time = self.runtime()
            if maxtime is not None and run_time > maxtime:
                self.kill()
                self._finalize(process_output)
                return

            # naptime
            if sleep:
                time.sleep(sleep)

        # finalize
        self._finalize(process_output)

        return self.returncode # set by ``.poll()``

    def read(self, process_output=None):
        """read from the output buffer"""

        self.output_buffer.seek(self.location)
        read = self.output_buffer.read()
        if self.output is not None:
            self.output += read
        if process_output:
            process_output(read)
        self.location += len(read)
        return read

    def commandline(self):
        """returns string of command line"""

        if isinstance(self.command, string):
            return self.command
        return subprocess.list2cmdline(self.command)

    __str__ = commandline

    def runtime(self):
        """returns time spent running or total runtime if completed"""

        if self.end is None:
            return time.time() - self.start
        return self.end - self.start


def main(args=sys.argv[1:]):
    """CLI"""

    description = """demonstration of how to do things with subprocess"""

    # available programs
    progs = {'yes': ["yes"],
             'ping': ['ping', 'google.com']}

    # parse command line
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--time", dest="time",
                        type=float, default=4.,
                        help="seconds to run for (or <= 0 for forever)")
    parser.add_argument("-s", "--sleep", dest="sleep",
                        type=float, default=1.,
                        help="sleep this number of seconds between polling")
    parser.add_argument("-p", "--prog", dest='program',
                        choices=progs.keys(), default='ping',
                        help="subprocess to run")
    parser.add_argument("--list-programs", dest='list_programs',
                        action='store_true', default=False,
                        help="list available programs")
    parser.add_argument("--wait", dest='wait',
                        action='store_true', default=False,
                        help="run with ``.wait()`` and a callback")
    parser.add_argument("--callback", dest='callback',
                        action='store_true', default=False,
                        help="run with polling and a callback")
    options = parser.parse_args(args)

    # list programs
    if options.list_programs:
        for key in sorted(progs.keys()):
            print ('{}: {}'.format(key, subprocess.list2cmdline(progs[key])))
        sys.exit(0)

    # select program
    prog = progs[options.program]

    # start process
    proc = Process(prog)

    # demo function for processing output
    def output_processor(output):
        print ('[{}]:\n{}\n{}'.format(proc.runtime(),
                                      output.upper(),
                                      '-==-'*10))
    if options.callback:
        process_output = output_processor
    else:
        process_output = None

    if options.wait:
        # wait for being done
        proc.wait(maxtime=options.time, sleep=options.sleep, process_output=output_processor)
    else:
        # start the main subprocess loop
        while proc.poll(process_output) is None:

            if options.time > 0 and proc.runtime() > options.time:
                proc.kill()

            if options.sleep:
                time.sleep(options.sleep)

            if process_output is None:
                # process the output with ``.read()`` call
                read = proc.read()
                output_processor(read)

    # correctness tests
    assert proc.end is not None

    # print summary
    output = proc.output
    n_lines = len(output.splitlines())
    print ("{}: {} lines, ran for {} seconds".format(subprocess.list2cmdline(prog), n_lines, proc.runtime()))

if __name__ == '__main__':
    main()
