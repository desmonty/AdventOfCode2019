from IntCode import *
from math import log

if __name__=='__main__':
    # Test Replicant
    replicant = IntCode([
        1001, 100, 1, 100,
        1009, 100,
        204, -1,
        1001, 100, 1, 100,
        1008, 100, 21, 101,
        1006, 101, 4,
        99
    ])
    assert replicant.original_program == replicant.run()

    # Test Big Product
    program_bm = IntCode([1102,34915192,34915192,7,4,7,99,0])
    assert int(log(program_bm.run()[0], 10))+1 == 16

    # Test Big Print
    program_bp = IntCode([104,1125899906842624,99])
    assert program_bp.run()[0] == 1125899906842624

    for i in range(10):
        assert IntCode([109, 4, 203, -4, 204, -4, 99]).run(inputs=[i])[0] == i

    program = IntCode('input.csv')    
    out = program.run(inputs=[1])
    print("Answer #9.1: ", out)