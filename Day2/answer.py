
class IntCode(object):
    """docstring for IntCode"""
    def __init__(self, program):
        super(IntCode, self).__init__()
        self.program = program

        # If str, assume it's a filename
        if type(program) == str:
            with open(program, mode='r') as input_file:
                self.program = input_file.read()
                self.program = [int(x) for x in self.program.split(",")]


    def run(self, return_only: bool=True):
        """
        Takes list of values, run IntCode on it and return
        the resulting list.

        If return_only is True, don't modify program and return output
        """
        if return_only:
            program_tmp = self.program.copy()

        instruction_pointer = 0
        while instruction_pointer < len(self.program):
            opCode = self.program[instruction_pointer]
            # Terminate self.program
            if opCode==99:
                if return_only:
                    output = self.get_output()
                    self.program = program_tmp
                    return output
                else:
                    return

            # Add numbers
            elif opCode==1:
                value_1 = self.get_value(instruction_pointer+1)
                value_2 = self.get_value(instruction_pointer+2)
                self.set_value(instruction_pointer+3, value_1 + value_2)
                instruction_pointer += 4

            # Multiply numbers
            elif opCode==2:
                value_1 = self.get_value(instruction_pointer+1)
                value_2 = self.get_value(instruction_pointer+2)
                self.set_value(instruction_pointer+3, value_1 * value_2)
                instruction_pointer += 4

            else:
                if return_only:
                    self.program = program_tmp
                raise ValueError("SegFault LOL")
        
        if return_only:
            self.program = program_tmp
        raise ValueError("Program didn't terminate")


    def set_inputs(self, noun: int, verb: int) -> list:
        """
        Set noun (position=1) and verb (position=2) in the program and return it.
        """
        self.program[1]=noun
        self.program[2]=verb


    def get_value(self, position: int) -> int:
        """
        Return the value at adress given by position 'position' in the program
        """
        return self.program[self.program[position]]


    def set_value(self, position: int, value: int) -> int:
        """
        Set the value at adress given by position 'position' in the program
        """
        self.program[self.program[position]] = value


    def get_output(self) -> int:
        """
        Return output (value at position 0)
        """
        return self.program[0]


    def reverse_engineer(self, desired_output: int, range_search: int=99) -> int:
        """
        Find noun and verb so that program ouput a specific number.
        'range' is used to reduce the search of inputs.

        Return 100 * noun + verb
        """
        for noun_candidate in range(range_search+1):
            for verb_candidate in range(range_search+1):
                self.set_inputs(noun_candidate, verb_candidate)
                try:
                    if self.run() == desired_output:
                        return 100*noun_candidate+verb_candidate
                except ValueError as e:
                    pass

        raise ValueError("Inputs not found")


if __name__=='__main__':
    program = IntCode("input.csv")
    program.set_inputs(12, 2)

    print("Answer #2.1: ", program.run())
    print("Answer #2.2: ", program.reverse_engineer(19690720))