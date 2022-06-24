export $(cat src/.env | xargs)
flask db migrate -m $1