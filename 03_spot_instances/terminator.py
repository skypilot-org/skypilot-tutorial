# Helper functions to terminate AWS instances
import sky
import subprocess
import time
import sys


def sleep_timer(time_duration):
    for remaining in range(time_duration, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:3d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)


def terminate(job_name=None, job_region=None):
    if job_name is None:
        print("Finding spot job to terminate...")
        jobs = sky.core.spot_status(refresh=False)
        latest_job = max(jobs, key=lambda k: k['job_id'])
        job_name = latest_job['job_name']
        job_region = latest_job['region']
        assert str(latest_job[
                       'status']) == 'SpotStatus.RUNNING', f'Job {job_name} is not running, please check sky spot status'
    assert job_name is not None, "No job name provided"
    assert job_region is not None, "No job region provided"
    print(f"Terminating latest spot job {job_name}...")
    run_aws_terminate(job_name, job_region)
    print(f"\n====== Successfully terminated spot VM. Hasta la vista, {job_name} ======")


def run_aws_terminate(job_name, job_region):
    # Get instance id
    print("Getting instance id...")
    instance_id_cmd = f'aws ec2 describe-instances --region {job_region} --filters Name=tag:ray-cluster-name,Values={job_name}* --query Reservations[].Instances[].InstanceId --output text'
    result = subprocess.run(instance_id_cmd, shell=True, stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(
            f'Unable to get instance_id for job {job_name}. Command: {instance_id_cmd}. Retcode: {result.returncode}. Stdout: {result.stdout}. Stderr: {result.stderr}')
    instance_id = result.stdout.decode('utf-8')
    print(f"Terminating instance_id {instance_id}")

    # Terminate instances
    terminate_cmd = f'aws ec2 terminate-instances --region {job_region} --instance-ids {instance_id}'
    print(f"Running command: {terminate_cmd}")
    result = subprocess.run(terminate_cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, universal_newlines=True,
                            shell=True)
    if result.returncode != 0:
        raise RuntimeError(
            f'Unable to terminate job {job_name}. Command: {terminate_cmd}. Retcode: {result.returncode}. Stdout: {result.stdout}. Stderr: {result.stderr}')
