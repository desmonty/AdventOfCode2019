class IntCode(object):
    """docstring for IntCode"""

    max_params = 3

    def __init__(self, program):
        super(IntCode, self).__init__()
        self.program = program

        # If str, assume it's a filename
        if type(program) == str:
            with open(program, mode='r') as input_file:
                self.program = input_file.read()
                self.program = [int(x) for x in self.program.split(",")]

    def run(self, inputs: list=None, return_only: bool=True):
        """
        Takes list of values, run IntCode on it and return
        the resulting list.

        If return_only is True, don't modify program and return output

        'inputs' is a list of inputs that will be given to the program as
        it needs them.
        """
        if return_only:
            program_tmp = self.program.copy()

        # Init program
        self.inputs = []
        self.outputs = []
        self.input_pointer = 0
        if inputs:
            self.inputs = inputs
            self.input_pointer = 0

        instruction_pointer = 0
        while instruction_pointer < len(self.program):
            # Get opCode and parameter modes
            instruction_code = str(self.program[instruction_pointer])
            parameter_modes = [0] * IntCode.max_params
            if len(instruction_code) <= 2:
                opCode = int(instruction_code)
            else:
                opCode = int(instruction_code[-2:])
                for i, param_tmp in enumerate(instruction_code[-3::-1]):
                    parameter_modes[i] = int(param_tmp)

            # Terminate self.program
            if opCode == 99:
                if return_only:
                    self.program = program_tmp
                    return self.get_output()
                else:
                    return

            # Add numbers
            elif opCode == 1:
                value_1 = self.get_value(
                    instruction_pointer + 1,
                    parameter_mode=parameter_modes[0]
                )
                value_2 = self.get_value(
                    instruction_pointer + 2,
                    parameter_mode=parameter_modes[1]
                )
                self.set_value(instruction_pointer + 3, value_1 + value_2)
                instruction_pointer += 4

            # Multiply numbers
            elif opCode == 2:
                value_1 = self.get_value(
                    instruction_pointer + 1,
                    parameter_mode=parameter_modes[0]
                )
                value_2 = self.get_value(
                    instruction_pointer + 2,
                    parameter_mode=parameter_modes[1]
                )
                self.set_value(instruction_pointer + 3, value_1 * value_2)
                instruction_pointer += 4

            # Input number
            elif opCode == 3:
                if self.input_pointer == len(self.inputs):
                    raise ValueError("Input not found")
                self.set_value(
                    instruction_pointer + 1,
                    self.inputs[self.input_pointer]
                )
                self.input_pointer += 1
                instruction_pointer += 2

            # Add output
            elif opCode == 4:
                self.outputs.append(
                    self.get_value(
                        instruction_pointer + 1,
                        parameter_mode=parameter_modes[0]
                    )
                )
                instruction_pointer += 2

            # jump-if-true
            elif opCode == 5:
                tmp_condition = self.get_value(
                    instruction_pointer + 1,
                    parameter_mode=parameter_modes[0]
                )
                if tmp_condition != 0:
                    instruction_pointer = self.get_value(
                        instruction_pointer + 2,
                        parameter_mode=parameter_modes[1]
                    )
                else:
                    instruction_pointer += 3

            # jump-if-false
            elif opCode == 6:
                tmp_condition = self.get_value(
                    instruction_pointer + 1,
                    parameter_mode=parameter_modes[0]
                )
                if tmp_condition == 0:
                    instruction_pointer = self.get_value(
                        instruction_pointer + 2,
                        parameter_mode=parameter_modes[1]
                    )
                else:
                    instruction_pointer += 3

            # less than
            elif opCode == 7:
                value_1 = self.get_value(
                    instruction_pointer + 1,
                    parameter_mode=parameter_modes[0]
                )
                value_2 = self.get_value(
                    instruction_pointer + 2,
                    parameter_mode=parameter_modes[1]
                )
                self.set_value(
                    instruction_pointer + 3,
                    1 if value_1 < value_2 else 0
                )
                instruction_pointer += 4

            # equals
            elif opCode == 8:
                value_1 = self.get_value(
                    instruction_pointer + 1,
                    parameter_mode=parameter_modes[0]
                )
                value_2 = self.get_value(
                    instruction_pointer + 2,
                    parameter_mode=parameter_modes[1]
                )
                self.set_value(
                    instruction_pointer + 3,
                    1 if value_1 == value_2 else 0
                )
                instruction_pointer += 4

            else:
                if return_only:
                    self.program = program_tmp
                raise ValueError("SegFault LOL")

        if return_only:
            self.program = program_tmp

        return self.program

    def set_inputs(self, noun: int, verb: int) -> list:
        """
        Set noun (position=1) and verb (position=2)
        in the program and return it.
        """
        self.program[1] = noun
        self.program[2] = verb

    def get_value(self, position: int, parameter_mode: int=0) -> int:
        """
        Return the value at adress given by position 'position' in the program
        """
        # Position mode
        if parameter_mode == 0:
            return self.program[self.program[position]]
        elif parameter_mode == 1:
            return self.program[position]
        else:
            raise ValueError("Parameter mode unrecognized: ", parameter_mode)

    def set_value(self, position: int, value: int) -> int:
        """
        Set the value at adress given by position 'position' in the program
        """
        self.program[self.program[position]] = value

    def get_output(self) -> int:
        """
        Return output (value at position 0)
        """
        return self.outputs

    def reverse_engineer(self, output: int, range_search: int = 99) -> int:
        """
        Find noun and verb so that program ouput a specific number.
        'range' is used to reduce the search of inputs.

        Return 100 * noun + verb
        """
        for noun_candidate in range(range_search + 1):
            for verb_candidate in range(range_search + 1):
                self.set_inputs(noun_candidate, verb_candidate)
                try:
                    if self.run() == output:
                        return 100 * noun_candidate + verb_candidate
                except ValueError:
                    pass
        # Program didn't find any possible inputs
        return -1
