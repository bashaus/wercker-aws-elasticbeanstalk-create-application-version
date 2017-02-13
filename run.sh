# Property: aws-access-key-id
# Check if the Access Key ID exists
if [[ -z "$WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_AWS_ACCESS_KEY_ID" ]];
then
  fail "Property aws-access-key-id or environment variable AWS_ACCESS_KEY_ID required"
fi

# Property: aws-secret-access-key
# Check if the Secret Access Key exists
if [[ -z "$WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_AWS_SECRET_ACCESS_KEY" ]];
then
  fail "Property aws-secret-access-key or environment variable AWS_SECRET_ACCESS_KEY required"
fi

# Property: aws-region
# Check if the Secret Access Key exists
if [[ -z "$WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_AWS_REGION" ]];
then
  fail "Property aws-region or environment variable AWS_DEFAULT_REGION required"
fi

# Property: application-name
# Ensure that a application-name has been provided
if [[ -z "$WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_APPLICATION_NAME" ]];
then
  fail "Property application-name must be defined"
fi

# Property: environment-name
# Ensure that a environment-name has been provided
if [[ -z "$WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_ENVIRONMENT_NAME" ]];
then
  fail "Property environment-name must be defined"
fi

# Property: s3-version-bucket
# Ensure that a s3-version-bucket has been provided
if [[ -z "$WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_S3_VERSION_BUCKET" ]];
then
  fail "Property s3-version-bucket must be defined"
fi

# Property: artefact
# Ensure that an artefact has been provided, and the file exists
if [[ -z "$WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_ARTEFACT" ]];
then
  fail "Property artefact must be defined"
fi

if [[ ! -f "$WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_ARTEFACT" ]];
then
  fail "Artefact does not exist: $WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_ARTEFACT"
fi

# Task: Elastic Beanstalk Deploy
# Offload to the python script
($WERCKER_STEP_ROOT/dist/run/run)
WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_RESULT=$?

# Task: Response
if [ "$WERCKER_AWS_ELASTICBEANSTALK_DEPLOY_RESULT" -eq 0 ]; then
  success "Deployed to Elastic Beanstalk"
else
  fail "Failed to deploy to Elastic Beanstalk"
fi
