# -*- coding: utf-8 -*-

"""
law-db command line tool to update the db file by searching for tasks in modules within the python
path.
"""


import os
import sys
from argparse import ArgumentParser

import luigi

import law
import law.util
from law.config import Config


def main():
    # parse arguments
    parser = ArgumentParser(description="law-db update tool")

    parser.add_argument("-p", action="store_true", help="also look in PYTHONPATH")

    args = parser.parse_args()

    # determine paths to lookup
    lookup = [p.strip() for p in Config.instance().keys("paths")]
    if args.p and "PYTHONPATH" in os.environ:
        lookup.extend(p.strip() for p in os.environ["PYTHONPATH"].split(":"))

    # loop through paths, import everything to load tasks
    for path in lookup:
        path = str(os.path.expandvars(os.path.expanduser(path)))
        if not path:
            continue

        for base, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filebase, fileext = os.path.splitext(filename)
                if fileext != ".py" or filebase == "__main__":
                    continue
                fullpath = os.path.join(base, filename)
                # try to find a matching path in sys.path to be able to import it
                modparts = os.path.join(base, filebase).strip("/").split("/")
                if modparts[-1] == "__init__":
                    modparts.pop()
                modid = ""
                while modparts:
                    modid = modparts.pop() + (modid and ".") + modid
                    try:
                        mod = __import__(modid, globals(), locals())
                        break
                    except ImportError as e:
                        continue

    # determine data to write: "module_id:task_family:param param ..."
    seen_families = []
    task_classes = []
    lookup = [law.Task]
    while lookup:
        cls = lookup.pop(0)
        lookup.extend(cls.__subclasses__())

        if cls.task_family in seen_families:
            continue
        seen_families.append(cls.task_family)

        if (hasattr(cls, "run") or issubclass(cls, luigi.WrapperTask)) and not cls._exclude_db:
            task_classes.append(cls)

    def dbline(cls):
        # determine parameters
        params = ["workers", "local-scheduler", "help"]
        for attr in dir(cls):
            member = getattr(cls, attr)
            if isinstance(member, luigi.Parameter):
                exclude = getattr(cls, "_exclude_params_db", set())
                if not law.util.multi_fnmatch(attr, exclude, any):
                    params.append(attr.replace("_", "-"))

        return cls.__module__ + ":" + cls.task_family + ":" + " ".join(params)

    # write the db file
    dbfile = Config.instance().get("core", "db_file")
    if not os.path.exists(os.path.dirname(dbfile)):
        os.makedirs(os.path.dirname(dbfile))
    with open(dbfile, "w") as f:
        for cls in task_classes:
            f.write(dbline(cls) + "\n")


if __name__ == "__main__":
    main()
