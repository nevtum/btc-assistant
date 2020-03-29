VIRTUALENV_HOME = .web_venv
ACTIVATE_CMD = source $(VIRTUALENV_HOME)/bin/activate
SRC_DIR = web_app
PYTHON_RUNTIME = python3.8
TEMPLATE_FILE = api_template.yaml

APP_NAME ?= btc-assistant-web-app
ARTIFACT_LOC ?= build-artifacts

# set up the virtualenvironment
$(VIRTUALENV_HOME)/.deps:
	virtualenv -p $(PYTHON_RUNTIME) $(VIRTUALENV_HOME) && \
	$(ACTIVATE_CMD) && \
	pip install -r $(SRC_DIR)/requirements.txt
	touch $(VIRTUALENV_HOME)/.deps

# set up the virtualenvironment
$(VIRTUALENV_HOME)/.build_deps: $(VIRTUALENV_HOME)/.deps
	virtualenv -p $(PYTHON_RUNTIME) $(VIRTUALENV_HOME) && \
	$(ACTIVATE_CMD) && \
	pip install -r $(SRC_DIR)/requirements.build.txt
	touch $(VIRTUALENV_HOME)/.build_deps

# force creation of virtualenvironment
venv:: $(VIRTUALENV_HOME)/.deps

build:: $(VIRTUALENV_HOME)/.build_deps
	$(ACTIVATE_CMD) && \
	sam build --use-container --debug \
		-t $(TEMPLATE_FILE)

package: $(VIRTUALENV_HOME)/.build_deps api_template.yaml
	$(ACTIVATE_CMD) && \
	sam package \
		--s3-bucket ${ARTIFACT_LOC} \
		--s3-prefix "${APP_NAME}" \
		--output-template-file template.packaged.yml
	aws s3 cp --acl bucket-owner-full-control template.packaged.yml s3://${ARTIFACT_LOC}/${APP_NAME}/template.packaged.yml
	echo "********************************************************"
	cat template.packaged.yml
	echo "********************************************************"
	rm -rf template.packaged.yml

deploy: $(VIRTUALENV_HOME)/.build_deps ## Create/update CloudFormation stack. Example: make deploy ENV=staging
	$(ACTIVATE_CMD) && \
	aws s3 cp s3://${ARTIFACT_LOC}/${APP_NAME}/${ARTIFACT_NUMBER}/template.packaged.yml . && \
	sam deploy \
		--template-file template.packaged.yml \
		--stack-name ${APP_NAME}-${ENV} \
		--parameter-overrides Stage=${ENV} Application=${APP_NAME} \
		--tags environment=${ENV} app=${APP_NAME} \
		--region ${AWS_REGION} \
		--capabilities CAPABILITY_NAMED_IAM
	rm -f template.packaged.yml

undeploy: $(VIRTUALENV_HOME)/.build_deps ## Delete CloudFormation stack. Example: make delete ENV=dev
	aws cloudformation delete-stack --stack-name ${x}-${ENV}
	aws cloudformation wait stack-delete-complete --stack-name ${APP_NAME}-${ENV}

clean::
	rm -rf $(VIRTUALENV_HOME) build dist .cache .eggs .tmp *.egg-info $(SRC_DIR)/*.egg-info
	rm -rf .aws-sam .pytest_cache .coverage htmlcov
	find . -name ".DS_Store" -exec rm -rf {} \; || true
	find . -name "*.pyc" -exec rm -rf {} \; || true
	find . -name "__pycache__" -exec rm -rf {} \; || true

.PHONY: help build package deploy undeploy