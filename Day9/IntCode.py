import copy

class IntCode(object):
    """docstring for IntCode"""

    max_params = 3
    size_program = 100000

    def __init__(self, program):
        super(IntCode, self).__init__()

        self.original_program = program
        # If str, assume it's a filename
        if type(program) == str:
            with open(program, mode='r') as input_file:
                self.original_program = [int(x) for x in input_file.read().split(",")]

        self.program = copy.deepcopy(self.original_program) + [0] * IntCode.size_program
        self.inputs = []
        self.outputs = []
        self.input_pointer = 0
        self.relative_base = 0
        self.instruction_pointer = 0

    def init_params(self):
        """
        Initialize parameters for program
        """
        self.inputs = []
        self.outputs = []
        self.input_pointer = 0
        self.relative_base = 0
        self.instruction_pointer = 0
        self.program = copy.deepcopy(self.original_program) + [0] * IntCode.size_program

    def op_add(self, parameter_modes: list) -> int:
        """
        Add numbers and return instruction_pointer position
        """
        value_1 = self.get_value(
            self.instruction_pointer + 1,
            parameter_mode=parameter_modes[0]
        )
        value_2 = self.get_value(
            self.instruction_pointer + 2,
            parameter_mode=parameter_modes[1]
        )
        self.set_value(
            self.instruction_pointer + 3,
            value_1 + value_2,
            parameter_modes[2]
        )
        self.instruction_pointer += 4

    def op_mult(self, parameter_modes: list) -> int:
        """
        multiply numbers and return instruction_pointer position
        """
        value_1 = self.get_value(
            self.instruction_pointer + 1,
            parameter_mode=parameter_modes[0]
        )
        value_2 = self.get_value(
            self.instruction_pointer + 2,
            parameter_mode=parameter_modes[1]
        )
        self.set_value(
            self.instruction_pointer + 3,
            value_1 * value_2,
            parameter_modes[2]
        )
        self.instruction_pointer += 4

    def op_input(self, parameter_modes: list) -> int:
        """
        Input number in the program
        """
        if self.input_pointer == len(self.inputs):
            raise ValueError("Input not found")
        self.set_value(
            self.instruction_pointer + 1,
            self.inputs[self.input_pointer],
            parameter_modes[0]
        )
        self.input_pointer += 1
        self.instruction_pointer += 2

    def op_output(self, parameter_modes: list) -> int:
        """
        Register number in output
        """
        self.outputs.append(
            self.get_value(
                self.instruction_pointer + 1,
                parameter_mode=parameter_modes[0]
            )
        )
        self.instruction_pointer += 2

    def op_jump_if_true(self, parameter_modes: list) -> int:
        """
        Move Instruction pointer to parameter_2 if parameter_1 is 1
        """
        tmp_condition = self.get_value(
            self.instruction_pointer + 1,
            parameter_mode=parameter_modes[0]
        )
        if tmp_condition != 0:
            self.instruction_pointer = self.get_value(
                self.instruction_pointer + 2,
                parameter_mode=parameter_modes[1]
            )
        else:
            self.instruction_pointer += 3

    def op_jump_if_false(self, parameter_modes: list) -> int:
        """
        Move Instruction pointer to parameter_2 if parameter_1 is 0
        """
        tmp_condition = self.get_value(
            self.instruction_pointer + 1,
            parameter_mode=parameter_modes[0]
        )
        if tmp_condition == 0:
            self.instruction_pointer = self.get_value(
                self.instruction_pointer + 2,
                parameter_mode=parameter_modes[1]
            )
        else:
            self.instruction_pointer += 3

    def op_less_than(self, parameter_modes: list) -> int:
        """
        Put 1 in parameter_3 if parameter_1 is equal to parameter_2, 0 otherwise
        """
        value_1 = self.get_value(
            self.instruction_pointer + 1,
            parameter_mode=parameter_modes[0]
        )
        value_2 = self.get_value(
            self.instruction_pointer + 2,
            parameter_mode=parameter_modes[1]
        )
        self.set_value(
            self.instruction_pointer + 3,
            1 if value_1 < value_2 else 0,
            parameter_modes[2]
        )
        self.instruction_pointer += 4

    def op_equals(self, parameter_modes: list) -> int:
        """
        Put 1 in parameter_3 if parameter_1 is equal to parameter_2, 0 otherwise
        """
        value_1 = self.get_value(
            self.instruction_pointer + 1,
            parameter_mode=parameter_modes[0]
        )
        value_2 = self.get_value(
            self.instruction_pointer + 2,
            parameter_mode=parameter_modes[1]
        )
        self.set_value(
            self.instruction_pointer + 3,
            1 if value_1 == value_2 else 0,
            parameter_modes[2]
        )
        self.instruction_pointer += 4

    def op_change_relative_base(self, parameter_modes: list) -> int:
        """
        Change the current relative base of the program.
        """
        self.relative_base = self.get_value(
            self.instruction_pointer + 1,
            parameter_mode=parameter_modes[0]
        )
        self.instruction_pointer += 2

    def run(self, inputs: list=None, return_only: bool=True, return_on_output: bool=False, verbose: bool=False):
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
        if inputs:
            self.inputs = inputs
            self.input_pointer = 0

        while self.instruction_pointer < len(self.program):
            # Get opCode and parameter modes
            instruction_code = str(self.program[self.instruction_pointer])
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
                    outputs = self.get_output()
                    self.init_params()
                    return outputs
                else:
                    return self.get_output()
            # Add numbers
            elif opCode == 1:
                self.op_add(parameter_modes)
            # Multiply numbers
            elif opCode == 2:
                self.op_mult(parameter_modes)
            # Input number
            elif opCode == 3:
                self.op_input(parameter_modes)
            # Add output
            elif opCode == 4:
                self.op_output(parameter_modes)
                if return_on_output:
                    return self.get_output()[-1]
            # jump-if-true
            elif opCode == 5:
                self.op_jump_if_true(parameter_modes)
            # jump-if-false
            elif opCode == 6:
                self.op_jump_if_false(parameter_modes)
            # less than
            elif opCode == 7:
                self.op_less_than(parameter_modes)
            # equals
            elif opCode == 8:
                self.op_equals(parameter_modes)
            elif opCode == 9:
                self.op_change_relative_base(parameter_modes)
            else:
                if return_only:
                    self.init_params()
                raise ValueError("SegFault LOL")

        outputs = self.get_output()
        if return_only:
            self.init_params()

        return outputs

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
        # Value mode
        elif parameter_mode == 1:
            return self.program[position]
        # Relative mode
        elif parameter_mode == 2:
            return self.program[self.program[position] + self.relative_base]
        else:
            raise ValueError("Parameter mode unrecognized: ", parameter_mode)

    def set_value(self, position: int, value: int, parameter_mode: int=0) -> int:
        """
        Set the value at adress given by position 'position' in the program
        """
        if parameter_mode == 0:
            self.program[self.program[position]] = value
        elif parameter_mode == 2:
            self.program[self.relative_base + self.program[position]] = value
        else:
            raise ValueError("Wrong parameter mode for Input operation: ", parameter_mode)

    def get_output(self) -> int:
        """
        Return output (value at position 0)
        """
        return self.outputs

    def add_input(self, new_input: int):
        """
        Add input in inputs
        """
        self.inputs.append(new_input)

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
