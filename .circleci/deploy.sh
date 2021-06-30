cd /home/t2elzeth/sanri/backend_sanri || exit

git pull origin master

docker-compose up --build -d
