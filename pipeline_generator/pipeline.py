from jinja2 import Template
from pathlib import Path
import os

PIPELINE_TEMPLATE_J2_FILE = 'templates/bitbucket-pipelines.yml.j2'
ROLES_DIR = 'roles/'


class Pipeline:
    def generate_pipeline(self):
        template_string = self._load_template_as_string()
        template = Template(template_string)
        steps = self._build_steps()
        generated_output = template.render(parallel_steps=steps)
        print(generated_output)

    def _build_steps(self):
        return [Step(f"Molecule Test Batch - {index}",
                     self._build_script_commands(index))
                for index, scenario_rel_path in
                enumerate(self._find_all_scenarios(), 1)]

    @staticmethod
    def _build_script_commands(index):
        return ScriptCommand(f"./bin/run-tests-in-batches --batch {index}").all_commands()

    @staticmethod
    def _find_all_scenarios():
        scenario_dirs = []
        for root, dirs, files in os.walk(Path(os.path.join(os.path.dirname(__file__), "..", ROLES_DIR))):
            [scenario_dirs.append(root) for f in files if f.endswith("molecule.yml")]
        return scenario_dirs

    @staticmethod
    def _load_template_as_string():
        path = Path(os.path.join(os.path.dirname(__file__), PIPELINE_TEMPLATE_J2_FILE))
        return path.read_text()


class Step:
    def __init__(self, name, script_commands=None):
        if script_commands is None:
            script_commands = []
        self.name = name
        self.scriptCommands = script_commands


class ScriptCommand:
    PACKAGE_INSTALL_COMMAND = "apt-get update && ./bin/install-ansible --dev"

    def __init__(self, test_command):
        self.test_command = test_command

    def all_commands(self):
        return [self.PACKAGE_INSTALL_COMMAND, self.test_command]


def main():
    Pipeline().generate_pipeline()


if __name__ == '__main__':
    main()
