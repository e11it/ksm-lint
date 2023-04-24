# KSM LINT CSV

Утилита проверки CSV файла ACL правил для [conduktor/kafka-security-manager](https://github.com/conduktor/kafka-security-manager).

## Примеры ошибок

Все тесты проводились командой:

```shell
$ docker run -it --rm -v$(pwd)/sample.csv:/tmp/sample.csv py-ksm:latest docker-lint /tmp/sample.csv
```

### Недопустимый символ `*` в имени топика 

Вызвавшая ошибку строка из sample.csv:
```csv
User:some-user,Topic,PREFIXED,some-topic-name-*,All,Allow,*
```

<details>
<summary>Вывод с ошибкой
</summary>
<p>

```shell
py_ksm.cli:ERROR:Error validate model
py_ksm.cli:ERROR:Line 5
{'KafkaPrincipal': 'User:some-user', 'ResourceType': 'Topic', 'PatternType': 'PREFIXED', 'ResourceName': 'some-topic-name-*', 'Operation': 'All', 'PermissionType': 'Allow', 'Host': '*'}
py_ksm.cli:ERROR:Error details:
[
  {
    "loc": [
      "ResourceName"
    ],
    "msg": "string does not match regex \"^(\\*|[a-zA-Z0-9._-]+)$\"",
    "type": "value_error.str.regex",
    "ctx": {
      "pattern": "^(\\*|[a-zA-Z0-9._-]+)$"
    }
  }
```
</p>
</details>

- Ошибка в ResourceName, тк loc: ResourceName.
- Причина, ResourceName не соответствует регулярному выражению `"pattern": "^(\|[a-zA-Z0-9._-]+)$"`
- Исходная строка: `'ResourceName': 'some-topic-name-*'`, звездочка в имени топика не разрешена.
- Ошибка находится в строке 5, файла `sample.csv`.


### Русская буква `с` в имени топика

Вызвавшая ошибку строка из sample.csv:
```csv
User:some-user,Topic,PREFIXED,some-topiс-name,All,Allow,*
```

<details>
<summary>Вывод с ошибкой
</summary>
<p>

```shell
py_ksm.cli:ERROR:Error validate model
py_ksm.cli:ERROR:Line 5
{'KafkaPrincipal': 'User:some-user', 'ResourceType': 'Topic', 'PatternType': 'PREFIXED', 'ResourceName': 'some-topiс-name', 'Operation': 'All', 'PermissionType': 'Allow', 'Host': '*'}
py_ksm.cli:ERROR:Error details:
[
  {
    "loc": [
      "ResourceName"
    ],
    "msg": "string does not match regex \"^(\\*|[a-zA-Z0-9._-]+)$\"",
    "type": "value_error.str.regex",
    "ctx": {
      "pattern": "^(\\*|[a-zA-Z0-9._-]+)$"
    }
  }
]
```
</p>
</details>

### Недопустимая операция Write над ресурсом Group

Вызвавшая ошибку строка из sample.csv:
```csv
User:some-user,Group,PREFIXED,some-group-name,Write,Allow,*
```

<details>
<summary>Вывод с ошибкой
</summary>
<p>

```shell
py_ksm.cli:ERROR:Error validate model
py_ksm.cli:ERROR:Line 4
{'KafkaPrincipal': 'User:some-user', 'ResourceType': 'Group', 'PatternType': 'PREFIXED', 'ResourceName': 'some-group-name', 'Operation': 'Write', 'PermissionType': 'Allow', 'Host': '*'}
py_ksm.cli:ERROR:Error details:
[
  {
    "loc": [
      "__root__"
    ],
    "msg": "Operation Write not allowed for resource Group",
    "type": "value_error"
  }
]
```
</p>
</details>

## Пример использования в gitlab ci. 

Предполагается, что файлы с ACL лежат в директории `ksm-acl` и попадают под маску `*.csv`.

Файл `.gitlab.ci`:
```yaml
.ksm-lint:
  image: e11it/py-ksm:v1
  before_script:
    - cd $CI_PROJECT_DIR
    - git config --global --add safe.directory $CI_PROJECT_DIR

ksm-linting:
  stage: lint
  extends: .py-ksm
  script:
    - >
      for file in $(git diff-tree --name-only --diff-filter=AMR --no-commit-id -r ${CI_COMMIT_SHA} | grep -E '^ksm-acl/.*\.csv'); do         
        echo "Linting acl file: ${file}";
        docker-lint "${file}";
      done
  allow_failure: false
  rules:
    - changes:
        - ksm-acl/*.csv
```

## Полезные ссылки

- [https://docs.confluent.io/platform/current/kafka/authorization.html](https://docs.confluent.io/platform/current/kafka/authorization.html)
- [https://kafka.apache.org/22/documentation.html#security_authz_cli](https://kafka.apache.org/22/documentation.html#security_authz_cli)
- [e11it/pydantic-common-models](https://github.com/e11it/pydantic-common-models)
