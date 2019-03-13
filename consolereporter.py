from pathlib import Path


class ConsoleReporter(object):
    def __init__(self, files_with_info: list) -> object:
        self.files_number = len(files_with_info)
        self.files_with_info = files_with_info

        self.current_violation_line = ""
        self.current_parsing_line = 0
        self.violations = 0

    def generate_report(self) -> str:
        output = ""

        if self.files_number > 0:
            for file_with_info in self.files_with_info:
                file, violations = file_with_info
                output = output + self.__generate_file_violations(file, violations)

        output = output + '\n' + self.__create_summary()
        return output

    def __create_summary(self) -> str:
        if self.violations == 0:
            return "Scanned %d file(s). Found no issues." % self.files_number
        else:
            return "Scanned %d file(s). Found %d issues." % (self.files_number, self.violations)

    def __generate_file_violations(self, file: Path, violations: list) -> str:
        output = ""
        with file.open() as cmake_file:
            self.current_violation_line = ""
            self.current_parsing_line = 0

            if violations:
                output = output + "\nFILE::::::::::" + str(file) + '\n'

            for (violation_type, line_number) in violations:
                self.violations = self.violations + 1
                self.__read_line_with_given_number(cmake_file, line_number)
                output = output + self.__generate_new_violation(line_number, violation_type)
        return output

    def __read_line_with_given_number(self, file, line):
        while self.current_parsing_line != line:
            self.current_parsing_line = self.current_parsing_line + 1
            self.current_violation_line = file.readline()

    def __generate_new_violation(self, line_number: int, violation_type: str):
        return "line: %d, %s:: %s" % (line_number, violation_type, self.current_violation_line)