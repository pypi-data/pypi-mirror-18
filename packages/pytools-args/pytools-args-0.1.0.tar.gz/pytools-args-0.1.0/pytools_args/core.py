# -*- coding: utf-8 -*-

import sys


class Arguments:

    def __init__(self):
        self._is_init = False
        self._arg_processor = None
        self._handlers = []

    def passed(self):
        return self.num_args() > 0

    def num_args(self):
        if self.get_args() is None:
            return 0

        return len(self.get_args())

    def num_sub_args(self):
        if self.get_sub_args() is None:
            return 0

        return len(self.get_sub_args())

    def has_args(self):
        return self.passed()

    def has_main_arg(self):
        return self.get_main_arg() is not None

    def has_sub_args(self):
        return self.get_sub_args() is not None

    def get_args(self):
        self._init_check()

        args = self._args

        if len(args) == 0:
            return None

        return args

    def get_main_arg(self):
        self._init_check()

        main_arg = self._main_arg

        if len(main_arg) == 0:
            return None

        return main_arg[0]

    def get_sub_arg(self, nth=0):
        sub_args = self.get_sub_args()

        if sub_args is None:
            return None

        if len(sub_args) <= nth:
            return None

        return sub_args[nth]

    def get_sub_args(self):
        self._init_check()

        sub_args = self._sub_args

        if len(sub_args) == 0:
            return None

        return sub_args

    def add_handler(self, handler):
        if isinstance(handler, ArgumentHandler):
            self._handlers.append(handler)

        elif type(handler) is list:
            for h in handler:
                if isinstance(h, ArgumentHandler):
                    self._handlers.append(h)

    def handle_args(self):
        for handler in self._handlers:
            if handler.check():
                return handler.handle()

        return None

    def set_arg_processor(self, fn=None):
        self._is_init = False
        self._arg_processor = fn

    def _default_arg_processor(self):
        args = sys.argv[1:]

        return args, args[0:1], args[1:]

    def _process_args(self):
        if self._arg_processor is None:
            return self._default_arg_processor()

        return self._arg_processor()

    def _init_check(self):
        if not self._is_init:
            args = self._process_args()

            self._args = args
            self._main_arg = args[0:1]
            self._sub_args = args[1:]

            self._is_init = True


class ArgumentHandler:

    def check(self):
        return False

    def handle(self):
        return None


_arguments = Arguments()

passed = _arguments.passed

num_args = _arguments.num_args
num_sub_args = _arguments.num_sub_args

has_args = _arguments.has_args
has_main_arg = _arguments.has_main_arg
has_sub_args = _arguments.has_sub_args

get_args = _arguments.get_args
get_main_arg = _arguments.get_main_arg
get_sub_args = _arguments.get_sub_args
get_sub_arg = _arguments.get_sub_arg

add_handler = _arguments.add_handler
handle_args = _arguments.handle_args

set_arg_processor = _arguments.set_arg_processor
