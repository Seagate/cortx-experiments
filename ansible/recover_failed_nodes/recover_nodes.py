import os
import sys
from error import error_mapping
from recovery import *

class Recover:
    def __init__(self):
        self.response = '/tmp/response'
        self.recover_mapping = {}

    def check_failed_nodes(self):
        from ast import literal_eval
        with open(self.response, 'r') as openfileobject:
            for line in openfileobject:
                python_dict = literal_eval(line)
                if python_dict['rc'] != 0:
                    host_machine = python_dict['host']
                    data = (python_dict['stdout'][0])
                    for error_class, msgs in error_mapping.items():
                        if any(val in data for val in msgs):
                            self.recover_mapping[host_machine] = error_class
        return self.recover_mapping


    def create_ini_files_for_failed_nodes(self):
        for key, values in self.recover_mapping.items():
            filename = f'/root/{values}Ini'
            with open(filename, 'a') as f:
                f.write(key)
                f.write("\n")

    def run_recovery(self):
        for values in self.recover_mapping.values():
            if os.path.exists(f'/root/{values}Ini'):
                recovery_class = Recover.str_to_class(values)
                recovery_class(f'/root/{values}Ini').run()

    @staticmethod
    def cleanup():
        path = os.listdir('/root')
        for file in path:
            if file.endswith("Ini"):
                os.remove(os.path.join('/root', file))

    @staticmethod
    def str_to_class(classname):
        return getattr(sys.modules[__name__], classname)


def main():
    recover = Recover()
    recover.cleanup()
    recover_nodes = recover.check_failed_nodes()
    if len(recover_nodes) == 0:
        print("Failed nodes are non-recoverable.\n"
              "Kindly fix the error and try again !!!")
        sys.exit(1)
    recover.create_ini_files_for_failed_nodes()
    recover.run_recovery()


if __name__ == "__main__":
    main()
