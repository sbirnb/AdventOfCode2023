import sys
from abc import ABC, abstractmethod
from operator import mul
from typing import Sequence, Iterable, Tuple, Mapping
import re


class Module(ABC):

    def __init__(self, outputs: Sequence[str]):
        self._outputs = outputs
        self._inputs = []

    @property
    def outputs(self) -> Sequence[str]:
        return self._outputs
    
    @property
    def inputs(self):
        return self._inputs


    @abstractmethod
    def pulse(self, source: str, high: bool) -> Iterable[Tuple[str, bool]]:
        pass

    def register_input(self, source: str) -> None:
        self._inputs.append(source)


class BroadcasterModule(Module):

    def pulse(self, source: str, high: bool) -> Iterable[Tuple[str, bool]]:
        return ((output, high) for output in self._outputs)


class FlipFlopModule(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on = False


    def pulse(self, source: str, high: bool) -> Iterable[Tuple[str, bool]]:
        if high:
            return tuple()
        self._on = not self._on
        return ((output, self._on) for output in self._outputs)


class ConjunctionModule(Module):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._low_inputs = set()

    def pulse(self, source: str, high: bool) -> Iterable[Tuple[str, bool]]:
        if high:
            self._low_inputs -= {source}
        else:
            self._low_inputs |= {source}
        return ((output, bool(self._low_inputs)) for output in self._outputs)

    def register_input(self, source: str) -> None:
        super().register_input(source)
        self._low_inputs.add(source)


def parse_input(input_: Iterable[str]) -> Mapping[str, Module]:
    modules = {
        id_: {'': BroadcasterModule, '%': FlipFlopModule, '&': ConjunctionModule}[type_](tuple(outs.split(', ')))
        for type_, id_, outs in (re.match(r'([%&]?)(\w+) -> (.*)', row).groups() for row in input_)
    }
    for name, module in modules.items():
        for out in module.outputs:
            if out not in modules:
                continue
            modules[out].register_input(name)
    return modules


def reduce_to_target(modules: Mapping[str, Module], target: str) -> Mapping[str, Module]:
    new_modules = dict()
    inputs_ = [name for name, module in modules.items() if target in module.outputs]
    while inputs_:
        input_ = inputs_.pop(0)
        if input_ in new_modules:
            continue
        new_modules[input_] = new_module = modules[input_]
        inputs_.extend(new_module.inputs)
    return new_modules


def part1(input_: Iterable[str]) -> int:
    modules = parse_input(input_)
    counts = [0, 0]
    for _ in range(1000):
        queue = [('button', 'broadcaster', False)]
        while queue:
            source, target, high = queue.pop(0)
            counts[high] += 1
            if target not in modules:
                continue
            queue.extend((target, *outpulses) for outpulses in modules[target].pulse(source, high))
    return mul(*counts)


def part2(input_: Iterable[str]) -> int:
    modules = parse_input(input_)
    print(len(modules))
    print(len(reduce_to_target(modules, 'rx')))
    for presses in range(1, 1000000):
        queue = [('button', 'broadcaster', False)]
        while queue:
            source, target, high = queue.pop(0)
            if source in {'dr', 'nh', 'xm', 'tr'} and high:
                print(presses, source, high)
            if target == 'rx' and not high:
                return presses
            if target not in modules:
                continue
            queue.extend((target, *outpulses) for outpulses in modules[target].pulse(source, high))

if __name__ == '__main__':
    input_ = tuple(sys.stdin.readlines())
    #print(part1(input_))
    print(part2(input_))
    print('done')