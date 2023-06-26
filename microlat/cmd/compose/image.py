import logging
import os
import pathlib
import shutil

import click

from microlat.cmd.compose import options
from microlat.compose import bootstrap
from microlat.compose import ostree
from microlat.compose import vm
from microlat import constants
from microlat.log import complete_step
from microlat.log import log_step
from microlat.log import setup_log
from microlat import preflight


@click.command(help="Compose an image")
@click.pass_context
@options.verbose
@options.suite
@options.mirror
@options.packages
@options.branch
@options.repo
@click.option("--name",
              default="debian-ostree-qemu-uefi-amd64.img",
              help="name of image")
@click.option("--size",
              "image_size",
              default="20G",
              help="Size of the image")
@options.arch
def image(ctxt,
          verbose,
          suite,
          mirror,
          packages,
          branch,
          repo,
          name,
          image_size,
          arch):
    setup_log()

    if branch is None:
        branch = f"debian/{suite}"
        log_step(f"Branch not set setting it to {branch}")

    workspace = constants.WORKSPACE
    with complete_step(f"Setting up workspace {constants.WORKSPACE}"):
        workspace = constants.WORKSPACE
        if workspace.exists():
            if click.confirm(
                f"Found previous workspace, Delete?"):
                shutil.rmtree(workspace)
        log_step(f"{workspace} does not exist, creating")
        workspace.mkdir(parents=True, exist_ok=True)

        output = pathlib.Path(constants.ARTIFACT)
        if output.exists():
            if click.confirm(f"Found {output}. copy it?"):
                shutil.copyfile(output, workspace.joinpath(output))

        try:
            # Check for required programs
            preflight.preflight_check()

            # Run mmdebstrap to build the rootfs.tar.gz
            rootfs = workspace.joinpath(output)
            if rootfs.exists():
                os.unlink(rootfs)
                if click.confirm(f"Do you want to recreate the {output}"):
                    bootstrap.run_mmdebstrap(
                        suite, mirror, rootfs, workspace, packages)
            else:
                bootstrap.run_mmdebstrap(
                    suite, mirror, rootfs, workspace, packages, arch)

            # Create ostree repo
            ostree.create_ostree_repo(rootfs, workspace, repo)

            # Commit rootfs to repo
            ostree.create_ostree_commit(workspace, branch, repo, arch, suite)

            # Run debos to create the image
            vm.run_vm(branch, repo, name, image_size, workspace, arch, suite)

        except Exception as ex:
            logging.error(f"Failed to compose: {ex}")
            raise ex
