# Описание работы
Реализована симуляция двух обособленных rest api сервисов line_provider, bet_maker, взаимодействие которых обеспечено через api запросы. 
Для их обособленного запуска, а также запуска redis используется docker-compose.

# Клонировать репозиторий
git clone github.com/gedovirhir/BettingSoftware_Test

# Перейти в папку с проектом
cd ./BettingSoftware_Test

# Запуск докер сервиса
docker-compose build

docker-compose up -d

- сервис line_provider будет запущен на localhost:8080
- сервис bet_maker будет запущен на localhost:8081

Если вы запускаете на Windows и на localhost не запускается, попробуйте заменить в .env переменную MAIN_HOST на результат команды docker-machine ip

# Тестирование и документация Api:

/api/doc

/api/redoc
