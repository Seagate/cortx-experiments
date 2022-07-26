import sys
import ansible_runner


class Runner:

    @staticmethod
    def run(playbook, ini):
        out, err, rc = ansible_runner.run_command(
        executable_cmd='ansible-playbook',
        cmdline_args=[playbook, '-i', ini],
        input_fd=sys.stdin,
        output_fd=sys.stdout,
        error_fd=sys.stderr
    )
        return rc