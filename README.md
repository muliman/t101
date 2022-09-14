# t101
* чтобы собрать Docker образ нужно использовать команду:
```
  docker build -t lab1 .
```
в данном случае создастся образ с именем lab1 в текущей директории
* для запуска Docker контейнера по существующему образу нужно использовать команду:
```
  docker run -it --rm lab1
```
благодаря параметру **--rm** контейнер удалится после завершения работы скрипта
