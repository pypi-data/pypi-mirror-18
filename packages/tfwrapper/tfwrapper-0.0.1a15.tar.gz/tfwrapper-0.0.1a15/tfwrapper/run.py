import subprocess
import logging
from distutils.spawn import find_executable
from .exceptions import TerraformRunException


LOG = logging.getLogger(__name__)

class TerraformRun(object):

    def __init__(self, terraform_arguments):
        self._terraform_path = find_executable('terraform')
        self._terraform_arguments = terraform_arguments

    def __call__(self):
        self._terraform_arguments.insert(0, self.terraform_path)
	LOG.info("Terraform command: {}".format(self._terraform_arguments))
        p = subprocess.Popen(self._terraform_arguments)
        stdout, stderr = p.communicate()
	LOG.info("Terraform exited with return code: {}".format(p.returncode))
	if p.returncode == 1:
		raise TerraformRunException

    @property
    def terraform_path(self):
        return self._terraform_path

    @terraform_path.setter
    def terraform_path(self, path):
        self._terraform_path = path
