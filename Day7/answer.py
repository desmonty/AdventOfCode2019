import copy
from itertools import permutations

from IntCode import *


def amplify_thrust(program: IntCode, phase_setting: list, feedback_loop: bool=False) -> int:
    """
    Run 5 amplifier program given phase setting and output
    final thrust.
    """
    output_amplifier = 0

    ampli_A = copy.deepcopy(program)
    ampli_A.add_input(phase_setting[0])
    ampli_B = copy.deepcopy(program)
    ampli_B.add_input(phase_setting[1])
    ampli_C = copy.deepcopy(program)
    ampli_C.add_input(phase_setting[2])
    ampli_D = copy.deepcopy(program)
    ampli_D.add_input(phase_setting[3])
    ampli_E = copy.deepcopy(program)
    ampli_E.add_input(phase_setting[4])

    while_continue = True
    while while_continue:
        ampli_A.add_input(output_amplifier)
        out_A = ampli_A.run(
            return_only=False,
            return_on_output=feedback_loop
        )
        if out_A is None or type(out_A) == list:
            out_A = ampli_A.get_output()[-1]
        ampli_B.add_input(out_A)
        out_B = ampli_B.run(
            return_only=False,
            return_on_output=feedback_loop
        )
        if out_B is None or type(out_B) == list:
            out_B = ampli_B.get_output()[-1]
        ampli_C.add_input(out_B)
        out_C = ampli_C.run(
            return_only=False,
            return_on_output=feedback_loop
        )
        if out_C is None or type(out_C) == list:
            out_C = ampli_C.get_output()[-1]
        ampli_D.add_input(out_C)
        out_D = ampli_D.run(
            return_only=False,
            return_on_output=feedback_loop
        )
        if out_D is None or type(out_D) == list:
            out_D = ampli_D.get_output()[-1]
        ampli_E.add_input(out_D)
        output_amplifier = ampli_E.run(
            return_only=False,
            return_on_output=feedback_loop
        )
        if output_amplifier is None:
            output_amplifier = ampli_E.get_output()[-1]
        if not feedback_loop or type(output_amplifier) == list:
            while_continue = False
            output_amplifier = output_amplifier[-1]

    return output_amplifier


def maximize_thrust(program: IntCode, phases: list, feedback_loop: bool=False) -> int:
    """
    Return maximal possible thrust.
    """
    list_phases = list(permutations(phases))
    list_thrust = [amplify_thrust(program, phase, feedback_loop) for phase in list_phases]
    return max(list_thrust)

if __name__ == '__main__':
    # 1
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

    # 2
    program_test_1 = IntCode([
        3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
        27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5
    ])
    assert maximize_thrust(program_test_1, [5, 6, 7, 8, 9], True) == 139629729

    program_test_2 = IntCode([
        3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5,
        55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54,
        53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53,
        1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10
    ])
    assert maximize_thrust(program_test_2, [5, 6, 7, 8, 9], True) == 18216

    program = IntCode("input.csv")
    print("Answer #7.2: ", maximize_thrust(program, [5, 6, 7, 8, 9], True))