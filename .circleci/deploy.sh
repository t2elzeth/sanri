cd /home/t2elzeth/sanri/sanri_backend || exit

git pull origin master

docker-compose up --build -d
