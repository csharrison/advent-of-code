from enum import Enum
from math import lcm
import itertools

class Type(Enum):
    BROADCASTER = 1
    FLIP_FLOP = 2
    CONJUNCTION = 3

class Pulse(Enum):
    LOW = 1
    HIGH = 2

class Module():
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations

class FlipFlop(Module):
    def __init__(self, name, destinations):
        super().__init__(name, destinations)
        self.toggled = False

    def pulse(self, pulse_type, from_module):
        if pulse_type == Pulse.HIGH:
            return
        self.toggled = not self.toggled
        new_pulse = Pulse.HIGH if self.toggled else Pulse.LOW
        for d in self.destinations:
            yield (d, new_pulse, self.name)

class Conjunction(Module):
    def __init__(self, name, destinations, module_map):
        super().__init__(name, destinations)
        self.memory = None
        self.module_map = module_map
        
    def maybe_init(self):
        if self.memory is None:
            self.memory = {m.name: Pulse.LOW for m in self.module_map.values()
                           if self.name in m.destinations}

    def pulse(self, pulse_type, from_module):
        self.maybe_init()
        self.memory[from_module] = pulse_type
        all_high = all(v == Pulse.HIGH for v in self.memory.values())
        new_pulse = Pulse.LOW if all_high else Pulse.HIGH
        for d in self.destinations:
            yield (d, new_pulse, self.name)

    def hashable(self):
        return tuple(self.memory.values())

class Broadcaster(Module):
    def __init__(self, name, destinations):
        super().__init__(name, destinations)

    def pulse(self, pulse_type, from_module):
        for d in self.destinations:
            yield (d, pulse_type, self.name)

def parse_modules(lines):
    module_map = {}
    
    for line in lines:
        name, destinations = line.strip().split(' -> ')
        destinations = destinations.replace(' ', '').split(',')
        if name == "broadcaster":
            module = Broadcaster(name, destinations)
        else:
            c, name = name[:1], name[1:]
            if c == "&":
                module = Conjunction(name, destinations, module_map)
            else:
                module = FlipFlop(name, destinations)
        module_map[module.name] = module
    return module_map

def press_button(module_map, process_func):
    queue = [("broadcaster", Pulse.LOW, "button")]
    while len(queue):
        dest, pulse_type, from_module = queue.pop(0)        

        if dest in module_map:
            new_pulses = list(module_map[dest].pulse(pulse_type, from_module))
            queue.extend(new_pulses)
        process_func(dest, pulse_type)

def compute_button_presses(module_map):
    first_seen = {}
    loop = {}
    computed = None

    # Some hardcoding based on the actual input because I'm lazy.
    # To do this properly we'd need to look at all of the inputs into rx, but this
    # could include multiple Conjunctions / FlipFlops, so the generic solution that
    # actually finds the minimum presses will be very complex.
    def check_loop(dest, pulse_type):
        vr_mem = module_map["vr"].memory
        if dest == "rx" and any(p == Pulse.HIGH for p in vr_mem.values()):
            for input, p in vr_mem.items():
                if p == Pulse.HIGH:
                    if input not in first_seen:
                        first_seen[input] = button_presses
                    elif input not in loop and first_seen[input] != button_presses:
                        loop[input] = button_presses - first_seen[input]
            if len(loop) == 4:
                nonlocal computed
                computed = lcm(*loop.values())

    for button_presses in itertools.count():
        press_button(module_map, check_loop)
        if computed is not None:
            return computed

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()
        modules = parse_modules(lines)
        pulses = {Pulse.LOW: 0, Pulse.HIGH: 0}
        def inc_pulse(dest, pulse_type):
            pulses[pulse_type] += 1
        for i in range(1000):
            press_button(modules, inc_pulse)
        print(pulses[Pulse.HIGH] * pulses[Pulse.LOW])
        # Reset the state
        modules = parse_modules(lines)
        print(compute_button_presses(modules))
