host = web@AWS

default: build

build:

ship: build
	rsync -avz --info=progress2 \
		--delete \
		--exclude='.git' --exclude='env/' --exclude='__pycache__/' --exclude='*.swp' --exclude='db.sqlite3' \
		backend/ ${host}:~/backend/
	rsync -avz --info=progress2 \
		--delete \
		--exclude='.git' --exclude='node_modules/' --exclude='__pycache__/' --exclude='*.swp' --exclude='db.sqlite3' \
		frontend/ ${host}:~/frontend/

deploy: ship
	@ssh -t ${host} "~/backend/deploy.sh"

.PHONY: build ship deploy
