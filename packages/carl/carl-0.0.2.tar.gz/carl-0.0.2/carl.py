from argparse import ArgumentParser, Namespace
from collections import namedtuple, OrderedDict, ChainMap
from functools import partial

from inspect import signature, Signature
from typing import Callable, Dict, no_type_check_decorator

from wrapt import decorator


STOP = 0b01
REQUIRED = 0b10


class NotArg:
    pass


@decorator
def printer(f, _, args, kwargs):
    print(f(*args, **kwargs))


@decorator
def empty_args(f, _, args, kwargs):
    if len(args) == 1 and not kwargs and callable(args[0]):
        return f()(args[0])
    else:
        return f(*args, **kwargs)


class ArgSpec(namedtuple('ArgSpec', 'annotation default')):
    pass


def arg_format(sig: Signature) -> Dict[str, ArgSpec]:
    return OrderedDict((a.name, ArgSpec(a.annotation, a.default))
                       for a in sig.parameters.values()
                       if a.annotation is not NotArg)


class SubparserNamespace:
    def __init__(self):
        super().__setattr__('subargs', Namespace())

    def __setattr__(self, k, v):
        setattr(self.subargs, k, v)  # pylint: disable=no-member


class Arg:
    def __init__(self, *args, optional=False, **kwargs) -> None:
        if args and args[0].startswith('-'):
            optional = True

        self.named = bool(args and isinstance(args[0], str))
        self.optional = optional
        self.args = args

        if 'choices' in kwargs:
            kwargs['choices'] = sorted(kwargs['choices'])

        self.kwargs = kwargs


def add_argument(parser, argspec: ArgSpec):
    (name, (arg, default)) = argspec

    if name == 'subcommand':
        parser.ensure_subparsers()
        if default is Signature.empty:
            parser.sub.required = True
        if isinstance(default, int):
            if default & STOP:
                parser.stop = True
            if default & REQUIRED:
                parser.sub.required = True
        return

    if arg is Signature.empty:
        arg = Arg()

    if isinstance(arg, str):
        arg = Arg(help=arg)

    if isinstance(arg, type):
        arg = Arg(type=arg)

    if default is not Signature.empty:
        arg.kwargs['default'] = default
        arg.optional = True

    if arg.optional:
        arg.kwargs['dest'] = name

    name = '--' + name if arg.optional else name

    if not arg.named:
        arg.args = [name] + list(arg.args)

    parser.add_argument(*(arg.args), **(arg.kwargs))


class MissingSubcommandError(Exception):
    pass


class CommandOptions:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def make_parser(factory, function, wrapper=None, is_sub=False):
    sig = signature(function)
    cmd_function = wrapper(function) if wrapper else function

    options = sig.return_annotation

    if options is Signature.empty:
        if function.__doc__:
            description = function.__doc__
            if is_sub:
                options = CommandOptions(help=description,
                                         description=description)
            else:
                options = CommandOptions(description=description)
        else:
            options = CommandOptions()

    if isinstance(options, str):
        options = CommandOptions(help=options,
                                 description=options)

    parser = factory(*options.args,
                     **options.kwargs)

    parser.inner = cmd_function
    parser.unwrapped = function
    parser.format = arg_format(sig)
    parser.is_sub = is_sub

    for argspec in parser.format.items():
        add_argument(parser, argspec)

    parser.set_defaults(_parser=parser)
    return parser


class Command(ArgumentParser):
    def __init__(self, f: Callable[..., None]=None, is_sub=False,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sub = None
        self.format = None
        self.is_sub = is_sub
        self.subcommands = []
        self.inner = f
        self.unwrapped = f
        self.stop = False

    def ensure_subparsers(self):
        if self.sub is None:
            self.sub = self.add_subparsers(dest='subcommand')

    def run(self, argv=None):
        arguments = self.parse_args(argv)

        self.resume(arguments)

    @staticmethod
    def resume(arguments, **extra):
        current = arguments
        while current is not None:
            vargs = vars(current)
            argd = {a: vargs[a]
                    for a in current._parser.format}

            if 'subcommand' in argd and argd['subcommand'] is not None:
                argd['subcommand'] = (current.subargs._parser,
                                      current.subargs)

            current._parser.inner(**ChainMap(argd, extra))

            if current._parser.stop:
                current = None
            else:
                current = getattr(current, 'subargs', None)
                extra = {}

    def parse_known_args(self, argv=None, namespace=None):
        if namespace is None and self.is_sub:
            namespace = SubparserNamespace()
        return super().parse_known_args(argv, namespace)

    @empty_args
    @no_type_check_decorator
    def subcommand(self, names=(), wrapper=None) -> 'Command':
        def inner(f):
            name, *aliases = (f.__name__,) if not names else names
            self.subcommands.extend([name] + aliases)
            self.ensure_subparsers()
            parser = make_parser(partial(self.sub.add_parser, name,
                                         aliases=aliases),
                                 f, wrapper, is_sub=True)
            return parser
        return inner

    def register_subcommands(self, *subcommands):
        for sub in subcommands:
            self.subcommand(sub)

    def __call__(self, *args, **kwargs):
        return self.unwrapped(*args, **kwargs)


@empty_args
@no_type_check_decorator
def command(wrapper=None):
    def inner(f):
        return make_parser(Command, f, wrapper=wrapper)
    return inner
