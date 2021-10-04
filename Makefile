build:
	./scripts/python.sh
	yarn
	yarn build
run:
	./scripts/run-dev.sh
clean:
	rm -rf node_modules
	rm -rf venv
	rm -rf app/static/js
purge:
	rm -rf node_modules
	rm -rf venv
	rm -rf app/static/js
	git clean -d -f
	git reset --hard

