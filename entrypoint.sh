while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  >&2 echo "Waiting for postgres..."
  sleep 1
done
echo "PostgreSQL started"

gunicorn 'app.__main__:get_app()'
