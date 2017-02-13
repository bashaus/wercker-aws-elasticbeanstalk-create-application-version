import boto3
import botocore
import time
from sys import exit
import logging

def eb_application_version_exists():
    """
    Checks Elastic Beanstalk to see if the Version already exists in
    the Application.
    """

    log.info(
        "Checking if application '%s' has version '%s'?",
        _ApplicationName,
        _EBVersionLabel
    )

    response = ElasticBeanstalkClient.describe_application_versions(
        ApplicationName=_ApplicationName,
        VersionLabels=[_EBVersionLabel],
        MaxRecords=1
    )

    if len(response["ApplicationVersions"]) == 1:
        log.info("Version exists")
        return True

    else:
        log.info("Version does not exist")
        return False


def s3_upload():
    """
    Uploads the Artefact to S3 so that it can be used by Elastic Beanstalk.
    """

    log.info("Uploading %s to S3", _Artefact)

    S3VersionBucket.upload_file(
        Filename=str(_Artefact),
        Key=_S3VersionKey
    )

def eb_check_version_processed():
    """
    When a Version is created in an Elastic Beanstalk Application, it is
    processed asynchronously. This loops until the Version is marked
    as PROCESSED.
    """

    for _ in range(10):
        log.debug(
            "Checking version '%s' is processed",
            _EBVersionLabel
        )

        VersionStatus = ElasticBeanstalkClient.describe_application_versions(
            ApplicationName=_ApplicationName,
            VersionLabels=[_EBVersionLabel],
            MaxRecords=1
        )["ApplicationVersions"][0]["Status"]

        log.debug(VersionStatus)

        if VersionStatus == "PROCESSED":
            break

        if VersionStatus == "FAILED":
            log.error("Aborting: application version returned failed status")
            exit(1)

        time.sleep(5)
    else:
        log.error("Aborting: could not determine status of application version")
        exit(1)

def eb_create_application_version():
    """
    Create a new Version in the Elastic Beanstalk Application.
    """

    if not eb_application_version_exists():
        s3_upload();

    log.debug(
        "Elastic Beanstalk: creating version '%s' in application '%s'",
        _EBVersionLabel,
        _ApplicationName
    )

    ElasticBeanstalkClient.create_application_version(
        ApplicationName=_ApplicationName,
        VersionLabel=_EBVersionLabel,
        Description=_VersionDescription,
        SourceBundle={
            'S3Bucket': _S3BucketName,
            'S3Key': _S3VersionKey
        },
        Process=True
    )

    eb_check_version_processed();


def eb_environment_ready():
    """
    Loops until the Elastic Beanstalk Environment is marked as Ready.
    """

    for _ in range(10):
        log.debug(
            "Checking environment '%s' is ready",
            _EnvironmentName
        )

        EnvironmentStatus = ElasticBeanstalkClient.describe_environment_health(
            EnvironmentName=_EnvironmentName,
            AttributeNames=["All"]
        )["Status"]

        log.debug(EnvironmentStatus)

        if EnvironmentStatus == "Ready":
            break

        if EnvironmentStatus in ("Launching", "Updating"):
            time.sleep(5)
            continue

        log.error("Aborting: invalid environment status '%s'", EnvironmentStatus)

    else:
        log.error("Aborting: failed to determine status of environment")
        exit(1)


def eb_environment_update():
    """
    Updates the Elastic Beanstalk Environment to use the new Version
    """

    eb_environment_ready();

    log.debug(
        "Updating environment '%s' to use version '%s'",
        _EnvironmentName,
        _EBVersionLabel
    )

    ElasticBeanstalkClient.update_environment(
        ApplicationName=_ApplicationName,
        EnvironmentName=_EnvironmentName,
        VersionLabel=_EBVersionLabel
    )


if __name__ == "__main__":

    # Setup logging
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    logging.getLogger("boto3").propagate = False
    logging.getLogger("botocore").propagate = False
    logging.getLogger("s3transfer").propagate = False
    log = logging.getLogger(os.environ["WERCKER_STEP_NAME"])

    # Prepare Variables
    _ApplicationName = os.environ["WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_APPLICATION_NAME"]
    _EnvironmentName = os.environ["WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_ENVIRONMENT_NAME"]
    _Artefact = os.environ["WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_ARTEFACT"]
    _S3BucketName = os.environ["WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_S3_VERSION_BUCKET"]
    _S3VersionKey = os.environ["WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_S3_VERSION_KEY"]
    _VersionDescription = os.environ["WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_VERSION_DESCRIPTION"]
    _EBVersionLabel = os.environ["WERCKER_GIT_COMMIT"]

    # Establish connection to Elastic Beanstalk
    AWSSession = boto3.Session(
        aws_access_key_id=os.environ["WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_AWS_REGION"]
    )

    # Establish connection to S3
    S3Resource = AWSSession.resource("s3")
    S3VersionBucket = S3Resource.Bucket(_S3BucketName)

    # Establish connection to Elastic Beanstalk
    ElasticBeanstalkClient = AWSSession.client("elasticbeanstalk")

    # If the version does not exist in Elastic Beanstalk, upload it
    eb_create_application_version();
    eb_environment_update();

    exit(0)
