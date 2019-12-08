from IntCode import *

if __name__ == '__main__':
    program = IntCode("input.csv")

    program.run(inputs=[1])
    output_1 = program.get_output()
    print("Answer #5.1: ", output_1[-1])

    program_is_8_position = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    assert IntCode(program_is_8_position).run(inputs=[7])[0] == 0
    assert IntCode(program_is_8_position).run(inputs=[8])[0] == 1
    assert IntCode(program_is_8_position).run(inputs=[9])[0] == 0

    program_lt_8_position = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
    assert IntCode(program_lt_8_position).run(inputs=[7])[0] == 1
    assert IntCode(program_lt_8_position).run(inputs=[8])[0] == 0
    assert IntCode(program_lt_8_position).run(inputs=[9])[0] == 0

    program_is_8_immediate = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
    assert IntCode(program_is_8_immediate).run(inputs=[7])[0] == 0
    assert IntCode(program_is_8_immediate).run(inputs=[8])[0] == 1
    assert IntCode(program_is_8_immediate).run(inputs=[9])[0] == 0

    program_lt_8_immediate = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    assert IntCode(program_lt_8_immediate).run(inputs=[7])[0] == 1
    assert IntCode(program_lt_8_immediate).run(inputs=[8])[0] == 0
    assert IntCode(program_lt_8_immediate).run(inputs=[9])[0] == 0

    program_test = [
	    3, 21, 1008, 21, 8, 20, 1005,
	    20, 22, 107, 8, 21, 20, 1006,
	    20, 31, 1106, 0, 36, 98, 0, 0,
	    1002, 21, 125, 20, 4, 20, 1105,
	    1, 46, 104, 999, 1105, 1, 46,
	    1101, 1000, 1, 20, 4, 20, 1105,
	    1, 46, 98, 99
   	]
    assert IntCode(program_test).run(inputs=[-13])[0] == 999
    assert IntCode(program_test).run(inputs=[7])[0] == 999
    assert IntCode(program_test).run(inputs=[8])[0] == 1000
    assert IntCode(program_test).run(inputs=[9])[0] == 1001
    assert IntCode(program_test).run(inputs=[191])[0] == 1001

    program.run(inputs=[5])
    output_2 = program.get_output()
    print("Answer #5.2: ", output_2[-1])
