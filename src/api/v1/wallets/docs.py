from fastapi import status

docs = {
    "all": {
        "summary": "Список кошельков",
        "description": "Получение списка всех кошельков и их балансов.",
        "response_description": "Список уникальный идентфикаторов кошельков и их балансов",
        "responses": {
            200: {
                "content": {
                    "application/json": {
                        "example": [
                            {
                                "uuid": "9486b0a0-2798-45f8-9e79-5ed0e8d46c23",
                                "balance": 1000,
                            },
                            {
                                "uuid": "87cb782d-83d4-486e-8436-c0d5a1d96f5d",
                                "balance": 0,
                            },
                        ]
                    }
                },
            }
        },
    },
    "balance": {
        "summary": "Баланс кошелька",
        "description": "Получение баланса кошелька по его uuid.",
        "response_description": "Баланс кошелька",
        "responses": {
            200: {
                "content": {
                    "application/json": {
                        "example": {
                            "balance": 1000,
                        },
                    }
                },
            }
        },
    },
    "create": {
        "status_code": status.HTTP_201_CREATED,
        "summary": "Создание кошелька",
        "description": "Создание кошелька.",
        "response_description": "Уникальный идентификатор созданного кошелька и его баланс",
        "responses": {
            201: {
                "content": {
                    "application/json": {
                        "example": {
                            "uuid": "9486b0a0-2798-45f8-9e79-5ed0e8d46c23",
                            "balance": 0,
                        },
                    }
                },
            }
        },
    },
    "operation": {
        "summary": "Изменение баланса кошелька",
        "description": 'Увеличение или уменьшение баланса кошелька на заданную величину.  Параметр operation_type определяет тип операции, может принимать значения "DEPOSIT" или "WITHDRAW"',
        "response_description": "Баланс кошелька после операции",
        "responses": {
            200: {
                "content": {
                    "application/json": {
                        "example": {
                            "balance": 100,
                        },
                    }
                },
            }
        },
    },
}
