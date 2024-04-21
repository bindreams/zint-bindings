import argparse
import subprocess as sp
import sys

VERSION = "v1"


def main():
    docker_arches = {"x86_64": "amd64", "aarch64": "arm64"}

    cli = argparse.ArgumentParser("build.py")
    cli.add_argument("--arch", nargs="+", choices=["x86_64", "aarch64"], help="image target architecture")

    args = cli.parse_args()

    for arch in args.arch:
        sp.run(
            [
                "docker",
                "build",
                "--progress",
                "plain",
                "--platform",
                f"linux/{docker_arches[arch]}",
                "--build-arg",
                f"CPUARCH={arch}",
                "--tag",
                f"ghcr.io/bindreams/zint-bindings/musllinux_1_1_{arch}:{VERSION}",
                ".",
            ],
            check=True,
        )


if __name__ == "__main__":
    sys.exit(main())
