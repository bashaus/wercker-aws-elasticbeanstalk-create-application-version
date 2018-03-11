# AWS ElasticBeanstalk Deploy

Wercker step to upload an artefact (ZIP, WAR, etc.) to an S3 bucket, create a 
new application version in ElasticBeanstalk and deploy it to an environment.

## Notes

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and
"OPTIONAL" in this document are to be interpreted as described in
RFC 2119.

## Sample Usage

    deploy:
      box: python:latest
      steps:
        - bashaus/aws-elasticbeanstalk-deploy:
          application-name: $DEPLOY_APPLICATION_NAME
          environment-name: $DEPLOY_ENVIRONMENT_NAME
          s3-version-bucket: $DEPLOY_S3_VERSION_BUCKET

&nbsp;

## Step Properties

### application-name (required)

The ElasticBeanstalk Application name.

* Since: `0.0.1`
* Property is `Required`
* Recommended location: `Application`
* `Validation` rules:
  * Must be accessible via `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
  * Must be in the `AWS_DEFAULT_REGION`

&nbsp;

### environment-name (required)

Elastic Beanstalk environment name where the version will be deploy (e.g.
project-name-stag, project-name-prod)

* Since: `0.0.1`
* Property is `Required`
* Recommended location: `Pipeline`
* `Validation` rules:
  * Must be an environment of the `application-name` application

&nbsp;

### s3-version-bucket (required)

The S3 bucket where the ElasticBeanstalk versions are held (e.g.
elasticbeanstalk-eu-west-1-############)

* Since: `0.0.1`
* Property is `Required`
* Recommended location: `Application`
* `Validation` rules:
  * Must only be the bucket name
  * Must be accessible via `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
  * Must be in the `AWS_DEFAULT_REGION`
  * Should be in the format of: elasticbeanstalk-[region]-[id]

&nbsp;

### artefact

The absolute path of the packaged application version in `.war` or `.zip`
format that will form the version.

* Since: `0.0.1`
* Property is `Optional`
* Default is: `$WERCKER_ROOT/$WERCKER_GIT_COMMIT.zip`
* Recommended location: `Inline`

&nbsp;

### s3-version-key

The path where the version will be stored in the S3 bucket.

* Since: `0.0.1`
* Property is `Optional`
* Default is: `$WERCKER_GIT_REPOSITORY/$WERCKER_GIT_COMMIT.zip`
* Recommended location: `Inline`
* `Validation` rules:
  * Must not begin with a slash (`/`)

&nbsp;

### version-description

A description of the version that is uploaded to ElasticBeanstalk. This is to
make it easier to identify using an ElasticBeanstalk tool (e.g.: the management
console or CLI).

* Since: `0.0.1`
* Property is `Optional`
* Recommended location: `Inline`
* `Default` value is: `User-Agent: Wercker`

&nbsp;

### aws-access-key-id

The AWS_ACCESS_KEY_ID to use in this deployment

* Since: `0.0.1`
* Property is `Required`, but is `Optional` if `AWS_ACCESS_KEY_ID` is set
* Default value is: `AWS_ACCESS_KEY_ID`
* Recommended location: `Application`

&nbsp;

### aws-secret-access-key

The AWS_SECRET_ACCESS_KEY to use in this deployment

* Since: `0.0.1`
* Property is `Required`, but is `Optional` if `AWS_SECRET_ACCESS_KEY` is set
* Default value is: `AWS_SECRET_ACCESS_KEY`
* Recommended location: `Application`
* `Validation` rules:
  * Must be stored as a protected environment variable

&nbsp;

### aws-region

The region where the bucket is located. If not set, will use AWS_DEFAULT_REGION.
Most likely eu-west-1

* Since: `0.0.1`
* Property is `Required`, but is `Optional` if `AWS_DEFAULT_REGION` is set
* Default value is: `AWS_DEFAULT_REGION`
* Recommended location: `Application`

&nbsp;
