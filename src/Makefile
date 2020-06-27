VIRTUALENV_HOME = .venv
BIN_DIR = $(VIRTUALENV_HOME)/bin
PYTHON_RUNTIME = python3.8
PYTHON = $(BIN_DIR)/python
ENV ?= staging
BUILD_NR ?= 1
ARTIFACT_NUMBER = build-${BUILD_NR}
DEPLOYMENT_BUCKET_NAME ?= btc-assistant
APP_NAME = data-collector-lambda
AWS_REGION ?= ap-southeast-2

target:
	@$(info useful info message here)

init.env:
	@$(call create_venv)
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install aws-sam-cli awscli --upgrade

build.worker:
	$(BIN_DIR)/sam validate --template-file worker_template.yaml && \
	$(BIN_DIR)/sam build CollectDataFunction -t worker_template.yaml

package.worker:
	$(BIN_DIR)/sam package \
		--s3-bucket ${DEPLOYMENT_BUCKET_NAME} \
		--s3-prefix "${APP_NAME}/${ARTIFACT_NUMBER}" \
		--output-template-file worker.packaged.yml
	$(BIN_DIR)/aws s3 cp --acl bucket-owner-full-control worker.packaged.yml \
		 s3://${DEPLOYMENT_BUCKET_NAME}/${APP_NAME}/${ARTIFACT_NUMBER}/worker.packaged.yml
	@echo "********************************************************"
	@cat worker.packaged.yml
	@echo "********************************************************"
	rm -rf worker.packaged.yml

deploy.worker:
	$(info [*] Copying deployment artifact from S3...)
	$(BIN_DIR)/aws s3 cp s3://${DEPLOYMENT_BUCKET_NAME}/${APP_NAME}/${ARTIFACT_NUMBER}/worker.packaged.yml . && \
	$(BIN_DIR)/sam deploy \
		--template-file worker.packaged.yml \
		--stack-name ${APP_NAME}-${ENV} \
		--parameter-overrides Stage=${ENV} Application=${APP_NAME} \
		--tags environment=${ENV} app=${APP_NAME} \
		--region ${AWS_REGION} \
		--capabilities CAPABILITY_NAMED_IAM
	rm -f worker.packaged.yml

delete.worker:
	$(BIN_DIR)/aws cloudformation delete-stack --stack-name ${APP_NAME}-${ENV}
	$(BIN_DIR)/aws cloudformation wait stack-delete-complete --stack-name ${APP_NAME}-${ENV}

deploy:
	@$(MAKE) init.env
	@$(MAKE) build.worker
	@$(MAKE) package.worker
	@$(MAKE) deploy.worker

define create_venv
	if [[ -d "./${VIRTUALENV_HOME}" ]]; then \
		echo "Virtual env already exists"; \
	else \
		${PYTHON_RUNTIME} -m venv ${VIRTUALENV_HOME}; \
	fi
endef