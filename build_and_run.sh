docker build -t starnavi .
docker run -d -p 8000:8000 starnavi
echo "server started on URL http://127.0.0.1:8000"