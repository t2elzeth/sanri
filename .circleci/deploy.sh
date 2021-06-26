cd /home/t2elzeth/sanri/backend || exit

git pull origin master

docker-compose up --build -d
