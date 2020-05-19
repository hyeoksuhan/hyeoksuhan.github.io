.DEFAULT_GOAL := help

SERVE := bundle exec jekyll serve

.PHONY: help
help: ## help information about make commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: draft
draft: ## run local server for draft
	@$(SERVE) --draft

.PHONY: serve
serve: ## run local server
	@$(SERVE)

.PHONY: build
build: ## build for deploy
	@sh -c './update_tags.py'
	@git add _tags

