import copy
from itertools import permutations

from IntCode import *


def amplify_thrust(program: IntCode, phase_setting: list) -> int:
    """
    Run 5 amplifier program given phase setting and output
    final thrust.
    """
    output_amplifier = 0
    for phase in phase_setting:
        output_amplifier = program.run(inputs=[phase, output_amplifier])[0]

    return output_amplifier


def maximize_thrust(program: IntCode, phases: list) -> int:
    """
    Return maximal possible thrust.
    """
    list_phases = list(permutations(phases))
    list_thrust = [amplify_thrust(program, phase) for phase in list_phases]
    return max(list_thrust)

if __name__ == '__main__':
    program_test_1 = IntCode([
        3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0
    ])
    assert maximize_thrust(program_test_1, list(range(5))) == 43210

    program_test_2 = IntCode([
        3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
        101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0
    ])
    assert maximize_thrust(program_test_2, list(range(5))) == 54321

    program_test_3 = IntCode([
    3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
    1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0
    ])
    assert maximize_thrust(program_test_3, list(range(5))) == 65210

    program = IntCode("input.csv")
    print("Answer #7.1: ", maximize_thrust(program, list(range(5))))
