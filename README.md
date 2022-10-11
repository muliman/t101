# t101
* Чтобы собрать Docker образ нужно использовать команду(для удобства из текущей директории проекта):
```
  docker build -t lab1 .
```
В данном случае создастся образ с именем lab1 
* Для запуска Docker контейнера по существующему образу нужно использовать команду:
```
  docker run -it --rm lab1
```
Благодаря параметру **--rm** контейнер удалится после завершения работы скрипта

### Проверка правил и фактов

Изначально правила генерируются для 4-х случаев( simple, random, ring, stairway ) и потом отдельно для них проверяются факты

#### Алгоритм работы функции проверки фактов *check_facts_vs_rules*:

Первым делом создается список **result** в котором будут хранится результаты правил по проверенным фактам

Далее правила для каждого типа разбиваются на 3 списка:

  * Правила с 'and'
  * Правила с 'or'
  * Правила с 'not'

Проверка фактов осуществляется проходом по получившимся спискам следующим образом:
  
 * Правила 'and' проверяются на полное вхождение фактов, а именно 
 
    Проходимся циклом по правилу 
    
    - Если элемент находится в списке фактов, то увеличиваем значение вспомогательной переменной **temp** на 1
    
    - После прохода сравниваем значение **temp** с количеством элементов в правиле
    
    - Если совпадают эти значения то записываем результат правила в **result**
    иначе записываем **0**
 * Правила 'or' проверяются до первого вхождения ( осуществляется аналогично с 'and', при первом вхождении выход из проверки )
 * Правила 'not' проверяются аналогично правилам 'and', но на полное невхождение ( аналогично 'and', значение вспомогательной переменной **temp** увеличивается, если элемент не входит)

В результирующий список проверенных фактов добавляется результат правила 'then'
в противном случае 0
