build:
	./scripts/python.sh
	yarn
	yarn build
run:
	./scripts/run-dev.sh
clean:
	rm -rf node_modules
	rm -rf venv
	rm -rf build
	rm app/static/js/*

