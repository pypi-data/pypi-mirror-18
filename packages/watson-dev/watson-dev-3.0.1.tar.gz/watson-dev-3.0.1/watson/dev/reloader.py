# -*- coding: utf-8 -*-
import sys
import os
import time
import _thread as thread

_mtimes = {}


def code_changed():
    global _mtimes
    filenames = [getattr(m, "__file__", None) for m in sys.modules.values()]
    for filename in filter(None, filenames):
        if filename.endswith(".pyc") or filename.endswith(".pyo"):
            filename = filename[:-1]
        if filename.endswith("$py.class"):
            filename = filename[:-9] + ".py"
        if not os.path.exists(filename):
            continue
        stat = os.stat(filename)
        mtime = stat.st_mtime
        if filename not in _mtimes:
            _mtimes[filename] = mtime
            continue
        if mtime != _mtimes[filename]:
            _mtimes = {}
            return True
    return False


def main(main_func, args=None, kwargs=None, script_dir=None):
    import __main__
    thread.start_new_thread(main_func, args or (), kwargs or {})
    while True:
        if code_changed():
            script = __main__.__file__
            print('\nCode changed, reloading...\n')
            if script_dir:
                script = os.path.join(script_dir, script)
            script = os.path.abspath(script)
            python = sys.executable
            args = [script] + sys.argv[1:]
            os.execl(python, python, *args)
            sys.exit(3)
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('\nTerminated.')
            sys.exit(0)
