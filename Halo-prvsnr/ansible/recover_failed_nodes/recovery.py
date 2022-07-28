from runner import Runner

class CreateResources:
    pass


class InstallPackages:
    def __init__(self, failed_nodes):
        self.failed_nodes = failed_nodes
 
    def run(self):
        Runner.run(playbook='install_packages.yml', ini=self.failed_nodes)
        
