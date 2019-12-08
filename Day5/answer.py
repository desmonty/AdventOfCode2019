from IntCode import *

if __name__ == '__main__':
    program = IntCode("input.csv")

    program.run(inputs=[1])
    output_1 = program.get_output()

    print("Answer #5.1: ", output_1[-1])

    # print("Answer #5.2: ", )
