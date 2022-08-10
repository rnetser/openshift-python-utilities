import datetime
import os
import shlex

# TODO: once approved and copied to main dir, update import
from for_review.infra import run_command
from for_review.logger import get_logger


LOGGER = get_logger(name=__name__)


def create_must_gather_command(
    dest_dir,
    image_url=None,
    script_name=None,
    kubeconfig=None,
    skip_tls_check=False,
):
    skip_tls_cmd = "--insecure-skip-tls-verify" if skip_tls_check else ""
    kubeconfig_cmd = f"--kubeconfig {kubeconfig}" if kubeconfig else ""
    image_cmd = f"--image={image_url}" if image_url else ""
    script_cmd = f"-- {script_name}" if script_name else ""
    cmd = f"oc adm must-gather {skip_tls_cmd} {kubeconfig_cmd} {image_cmd} --dest-dir={dest_dir} {script_cmd}"
    LOGGER.info(f"must-gather command: {cmd}")
    return cmd


def run_cnv_must_gather(must_gather_cmd):
    return run_command(command=shlex.split(must_gather_cmd))[1]


def save_must_gather_logs(
    target_base_dir, must_gather_image_url, kubeconfig=None, skip_tls_check=False, script_name=None,
):
    logs_path = os.path.join(
        target_base_dir,
        f"must_gather_{datetime.datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S')}",
    )
    os.makedirs(logs_path)
    must_gather_command = create_must_gather_command(
        image_url=must_gather_image_url,
        dest_dir=logs_path,
        kubeconfig=kubeconfig,
        skip_tls_check=skip_tls_check,
        script_name=script_name,
    )
    return run_cnv_must_gather(must_gather_cmd=must_gather_command)
