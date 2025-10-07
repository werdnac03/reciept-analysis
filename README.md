This is a reciept analysis webapp

activate venv -> source .venv/bin/activate
deactivate venv -> deactivate

frontend
    cd frontend2
    npm run dev

backend
    cd backend
    flask run

postgres db
    docker compose up