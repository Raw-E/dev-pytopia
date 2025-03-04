.PHONY: setupproject quicktest cursorrules poetryreset

# Initialize project by installing dependencies, running tests, and setting up Git repository
setupproject:
	poetry install && \
	pytest && \
	git init && \
	git add . && \
	git commit -m 'Initial commit!'

# Run only tests marked with 'quicktest' marker
quicktest:
	pytest -v -m quicktest

# Update AI instructions for Cursor
cursorrules:
	execute-command-on-change coding-guru-cli-runner update-ai-instructions
	
# Reset and reinstall Poetry environment
poetryreset:
	rm -rf .venv
	rm -f poetry.lock
	poetry install