frontend-dev:
	cd frontend && pnpm dev

backend-dev:
	cd backend && uv run uvicorn src:app --reload

dev:
	make -j 2 frontend-dev backend-dev