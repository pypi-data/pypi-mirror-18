import logging

from esrally import paths, config
from esrally.mechanic import supplier, provisioner, launcher

logger = logging.getLogger("rally.mechanic")


def create(cfg, metrics_store, sources=False, build=False, distribution=False, external=False, docker=False):
    if sources:
        s = lambda: supplier.from_sources(cfg, build)
        p = provisioner.local_provisioner(cfg)
        l = launcher.InProcessLauncher(cfg, metrics_store)
    elif distribution:
        s = lambda: supplier.from_distribution(cfg)
        p = provisioner.local_provisioner(cfg)
        l = launcher.InProcessLauncher(cfg, metrics_store)
    elif external:
        s = lambda: None
        p = provisioner.no_op_provisioner(cfg)
        l = launcher.ExternalLauncher(cfg, metrics_store)
    elif docker:
        s = lambda: None
        p = provisioner.no_op_provisioner(cfg)
        l = launcher.DockerLauncher(cfg, metrics_store)
    else:
        # It is a programmer error (and not a user error) if this function is called with wrong parameters
        raise RuntimeError("One of sources, distribution, docker or external must be True")

    return Mechanic(cfg, s, p, l)


class Mechanic:
    """
    Mechanic is responsible for preparing the benchmark candidate (i.e. all benchmark candidate related activities before and after
    running the benchmark).
    """

    def __init__(self, cfg, supply, p, l):
        self._config = cfg
        self.supply = supply
        self.provisioner = p
        self.launcher = l

        # TODO dm: Check whether we can remove this completely
        # ensure we don't mix ES installs
        track_name = self._config.opts("benchmarks", "track")
        challenge_name = self._config.opts("benchmarks", "challenge")
        race_paths = paths.Paths(self._config)
        self._config.add(config.Scope.challenge, "system", "challenge.root.dir",
                         race_paths.challenge_root(track_name, challenge_name))
        self._config.add(config.Scope.challenge, "system", "challenge.log.dir",
                         race_paths.challenge_logs(track_name, challenge_name))

    def prepare_candidate(self):
        self.supply()

    def start_engine(self):
        selected_car = self.provisioner.prepare()
        return self.launcher.start(selected_car)

    def stop_engine(self, cluster):
        self.launcher.stop(cluster)
        self.provisioner.cleanup()
