from IntCode import *

if __name__ == '__main__':
    program = IntCode("input.csv")

    program.run(inputs=[1])
    output_1 = program.get_output()

    print("Answer #5.1: ", output_1[-1])

    program_is_8_position = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    assert IntCode(program_is_8_position).run(inputs=[7]).get_output()[0] == 0
    assert IntCode(program_is_8_position).run(inputs=[8]).get_output()[0] == 1
    assert IntCode(program_is_8_position).run(inputs=[9]).get_output()[0] == 0

    program_lt_8_position = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    assert IntCode(program_lt_8_position).run(inputs=[7]).get_output()[0] == 1
    assert IntCode(program_lt_8_position).run(inputs=[8]).get_output()[0] == 0
    assert IntCode(program_lt_8_position).run(inputs=[9]).get_output()[0] == 0

    program_is_8_immediate = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    assert IntCode(program_is_8_immediate).run(inputs=[7]).get_output()[0] == 0
    assert IntCode(program_is_8_immediate).run(inputs=[8]).get_output()[0] == 1
    assert IntCode(program_is_8_immediate).run(inputs=[9]).get_output()[0] == 0

    program_lt_8_immediate = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    assert IntCode(program_lt_8_immediate).run(inputs=[7]).get_output()[0] == 1
    assert IntCode(program_lt_8_immediate).run(inputs=[8]).get_output()[0] == 0
    assert IntCode(program_lt_8_immediate).run(inputs=[9]).get_output()[0] == 0

    # print("Answer #5.2: ", )
