cd /home/t2elzeth/sanri/backend_sanri || exit

git pull origin dev

docker-compose up --build -d
