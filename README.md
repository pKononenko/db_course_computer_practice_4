# db_course_computer_practice_4 (КП-4. Кононенко Павло КМ-81. Варіант 15)
Комп'ютерний практикум - 1 з дисципліни Бази Даних. Кононенко Павло КМ-81 (Варіант 15)

## Директорія до запуску ##
```bash
.
├── results
│   └── results.csv
├── .gitignore
├── README.md
├── utils.py
└── main.py
```

## Інструкція до запуску ##
1. В проекті створити директорію ```data``` та помістити в неї ```.csv``` файли з даними результатів ЗНО за декілька років.
2. Запустити MongoDB в Docker.
* Якщо MongoDB не встановлено, то скористатися командою: ```docker pull mongo```
* Якщо MongoDB встановлено.
  * Створити та запустити контейнер за допомогою команди: ```docker run --name mongodb -p 27017:27017 mongo ```
  * Якщо контейнер було створено та зупинено, то запустити його за допомогою команди: ```docker start mongodb```
4. Запустити через консоль файл ```main.py``` за допомогою команди: ```python main.py <host> <port>```

## Директорія після запуску ##
```bash
.
├── data
│   ├── Odata2019File.csv
│   └── Odata2020File.csv
├── results
│   └── results.csv
├── mongo_db_log.log
├── .gitignore
├── README.md
├── utils.py
└── main.py
```


