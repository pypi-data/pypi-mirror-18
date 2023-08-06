# encoding=utf-8

"""
Simple worker, performs background tasks.
"""

import time

from ardj.log import *
from ardj.database import commit, rollback
from ardj.models import Task
from ardj.util import utf, deutf


__all__ = ["add_task", "run_task"]


def add_task(command, *args):
    t = ":".join(map(utf, [command] + list(args)))

    task = Task.get_by_task(t)
    if task:
        log_info("Task {} exists with id {}.", task["task"], task["id"])
    else:
        task = Task()
        task["run_after"] = int(time.time())
        task["task"] = t
        task.put()
        commit()
        log_info("Task {} added: {}", task["id"], task["task"])


def run_task(arg=None, *args):
    if arg == "help":
        print "Find a task which is ready to execute and waits the most."
        print "Executes the task and deletes it, or postpones on error."
        print "If there aren't any tasks -- waits 5 seconds and repeats."
        print "Normally you run this in a loop, to handle more than one task."
        exit(1)

    elif arg is not None:
        print "This command takes no argument."
        exit(1)

    explain = True

    while True:
        task = Task.pick_one()
        if task:
            break

        if explain:
            log_debug("Waiting for tasks.")
            explain = False

        rollback()
        time.sleep(5)

    try:
        parts = map(deutf, task["task"].split(":"))
        command = parts[0]
        args = parts[1:]

        if command == "tags.write" and args:
            from ardj.tracks import write_tags
            log_info("Writing tags to track {}", args[0])
            write_tags(args[0])

        else:
            log_warning("Task {} ({}) not understood, postponing.", task["id"], task["task"])
            task.postpone()
            commit()
            return

        log_info("Task {} ({}) completed, deleting.", task["id"], utf(task["task"]))
        print "Task %u completed: %s" (task["id"], utf(task["task"]))

        task.delete()
        commit()

    except Exception, e:
        log_exception("Task {} failed: {} -- postponing.", task["id"], e)
        task.postpone()
        commit()
