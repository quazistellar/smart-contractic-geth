from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_address
import re
from enum import Enum
class EstateType(Enum):
    House = 0
    Flat = 1
    Loft = 2
class AdStatus(Enum):
    Opened = 0
    Closed = 1

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
contract = w3.eth.contract(address=contract_address, abi=abi)

print()
print("-------------- >> АГЕНТСТВО НЕДВИЖИМОСТИ << --------------")
print()
print(f"Адрес смарт-контракта: {contract.address}")
print()
print(f" > Баланс смарт-контракта: {w3.eth.get_balance(contract.address)}")
print(f" > Баланс первого аккаунта: {w3.eth.get_balance('0x8538984DDDd639867306Dad1E11b59c5f5AF0E6E')}")
print(f" > Баланс второго аккаунта: {w3.eth.get_balance('0x4B9D076A0Dbf113C0Da1f6Aa3A65A1A151BE6826')}")
print(f" > Баланс третьего аккаунта: {w3.eth.get_balance('0xcFAF0395Ce3154A30dd7F8D283E992419bb702A4')}")
print(f" > Баланс четвертого аккаунта: {w3.eth.get_balance('0x745C4De7eA31bDBFDF5b324c52838D6CB7430774')}")
print(f" > Баланс пятого аккаунта: {w3.eth.get_balance('0x177A70e61C26DbF8A108FD80d8cfC550Fa3E75b2')}")
print()

def login():
    try:
        print()
        print(" --------------- <<< АВТОРИЗАЦИЯ >>> ---------------")
        print()
        public_key = input("Введите публичный ключ: ")
        password = input("Введите пароль: ")
        w3.geth.personal.unlock_account(public_key, password)
        return public_key
    except Exception as e:
        print()
        print(f"Ошибка авторизации: {e}")
        print()
        return None

def checker(password):
    if len(password) < 12:
        return False
    if password == "password" or password == "password123" or password == "qwerty123" or password == "password123456" or password == "password123456789qwerty":
        return False
    if " " in password:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*]", password):
        return False
    return True


def register():
    print()
    print(" --------------- <<< РЕГИСТРАЦИЯ >>> ---------------")
    print()
    password = input("Придумайте и введите пароль для нового аккаунта: ")
    if not checker(password):
        print("\nПароль не соответствует требованиям! Учтите, что в нём должно быть:\n - не менее 12 символов\n - отстутвие пробелов\n - хотя бы одна заглавная и строчная буква\n - хотя бы одна цифра\n - хотя бы один специальный символ (!@#$%^&*)\n - избегание простых шаблонов (например, password123)\nПопробуйте ещё раз!\n")
        return
    else:
        account = w3.geth.personal.new_account(password)
        print(f"Ваш публичный ключ: {account}")

def send_eth(account):
    try:
        value = int(input("Введите количество эфира для отправки на смарт-контракт: "))
        tx_hash = contract.functions.toPay().transact({
            "from": account,
            "value": value,
        })
        print(f"Сумма [{value}] успешна переведена с Вашего аккаунта на смарт-контракт!")
    except Exception as e:
        print(f"Ошибка отправки эфира: {e}")

def withdraw_to(account):
    try:
        amount = int(input("Введите количество эфиров для снятия со смарт-контракта: "))
        tx_hash = contract.functions.withdraw(amount).transact({
            "from": account,
        })
        print(f"Сумма [{amount}] успешно переведена со смарт-контракта на Ваш аккаунт!")
    except Exception as e:
        print(f" Ошибка снятия средств: {e}")

def get_balance(account):
    balance = contract.functions.getBalance().call({
        "from": account,
    })
    print(f"Ваш баланс на смарт-контракте: {balance}")


def create_estate(account):
    try:
        print()
        size = int(input("Введите площадь недвижимости: "))
        estate_address = input("Введите адрес недвижимости: ")
        estate_type = int(input("Введите тип недвижимости:\n0. Дом\n1. Квартира\n2. Лофт\n"))
        if estate_type not in [0, 1, 2]:
            print("Неверный тип недвижимости")
            return
        tx_hash = contract.functions.createEstate(size, estate_address, estate_type).transact({
            "from": account,
        })
        print(f"Транзакция {tx_hash.hex()} отправлена")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash.hex())
        if receipt.status == 1:
            print()
            print(f"Недвижимость площадью {size}, по адресу {estate_address} успешно создана!")
            print()
        else:
            print("\nНе удалось создать недвижимость")
    except Exception as e:
        print(f"\nОшибка при создании недвижимости: {e}\n")


def get_estates(account):
    try:
        estates = contract.functions.getEstates().call({
        })
        for estate in estates:
            pp = str(estate)
            if pp.find(account, 0):
                print(f"------------------------------------")
                print(f"Размер недвижимости: {estate[0]}")
                print(f"Адрес недвижимости: {estate[1]}")
                print(f"Владелец: {estate[2]}")
                print(f"Тип недвижимости: {estate[3]}")
                print(f"Активность: {estate[4]}")
                print(f"ID объекта: {estate[5]}")
                print(f"------------------------------------")
    except Exception as e:
        print(f"Ошибка при получении списка недвижимости: {e}")


def create_ad(account):
    try:
        price = int(input("Введите цену недвижимости: "))
        id_estate = int(input("Введите ID недвижимости: "))
        tx_hash = contract.functions.createAd(id_estate-1, price).transact({
            'from': account
        })
        print(f"\nОбъявление на недвижимость с ID {id_estate} по цене {price} успешно создано!")
        try:
            status = False
            contract.functions.updateEstateStatus(id_estate-1, status).transact({
                'from': account
            })
        except Exception as e:
            print(f"Ошибка : {e}")
    except Exception as e:
        print(f"Ошибка : {e}")

def get_ad():
    adds = contract.functions.getAds().call({
    })
    for add in adds:
        print("----------------------------------")
        print(f"Владелец: {add[0]}")
        print(f"Покупатель: {add[1]}")
        print(f"Цена: {add[2]}")
        print(f"ID недвижимости: {add[3]}")
        print(f"Дата: {add[4]}")
        print(f"Статус недвижимости: {add[5]}")
        print(f"ID объявления: {add[6]}")
        print("----------------------------------")

def update_estate_status(account):
    try:
        id_estate = int(input("Введите ID недвижимости: "))
        status = bool(int(input("Введите новый статус недвижимости (0 - неактивна, 1 - активна): ")))
        tx_hash = contract.functions.updateEstateStatus(id_estate - 1, status).transact({
            "from": account,
        })
        print(f"Статус недвижимости с ID {id_estate} успешно изменен!")
    except Exception as e:
        print(f"Ошибка при изменении статуса недвижимости: {e}")

def update_ad_status(account):
    try:
        id_ad = int(input("Введите ID объявления: "))
        status = bool(int(input("Введите новый статус объявления (0 - активно, 1 - неактивно): ")))
        status = int(status)
        tx_hash = contract.functions.updateAdStatus(id_ad, status).transact({
            "from": account,
        })
        print(f"Статус объявления с ID {id_ad} успешно изменен!")
    except Exception as e:
        print(f"Ошибка при изменении статуса объявления: {e}")

def buy_estate(account):
    try:
        id_add = int(input("Введите ID объявления: "))
        if isinstance(id_add, int) == False:
            print(" Ошибка покупки: Нужно вводить число")
        else:
            tx_hash = contract.functions.buyEstate(id_add).transact({
                'from': account
            })
            print(f"Недвижимость по объявлению с ID {id_add} успешно куплена!")
    except Exception as e:
        print(f" Ошибка {e}")

def main():
    account = ""
    while True:
        if account == "" or account == None:
            print("-- ВХОД В СИСТЕМУ")
            choice = input("\nВыберите действие: \n1. Авторизация\n2. Регистрация\n3. Выход\n")
            if choice.isdigit():
                choice = int(choice)
                match choice:
                    case 1:
                        account = login()
                    case 2:
                        register()
                    case 3:
                        print()
                        print("------------------------")
                        print("Вы вышли из системы!!!")
                        exit()
                    case _:
                        print()
                        print("Введите цифру от 1 до 3")
                        print()
            else:
                print()
                print("Введите цифру от 1 до 3")
                print()
        else:
            choice = input("\nВыберите действие: \n1. Создать недвижимость\n2. Создать объявление\n3. Изменить статус недвижимости\n4. Изменить статус объявления\n5. Покупка недвижимости\n6. Вывести средства на свой смарт-контракт\n7. Посмотреть все недвижимости\n8. Посмотреть все объявления\n9. Посмотреть баланс на аккаунте\n10. Посмотреть баланс смарт-контракта\n11. Вывести средства с контракта на свой счет\n12. Выход\n")
            if choice.isdigit():
                choice = int(choice)
                match choice:
                    case 1:
                        create_estate(account)
                    case 2:
                        create_ad(account)
                    case 3:
                        update_estate_status(account)
                    case 4:
                        update_ad_status(account)
                    case 5:
                        buy_estate(account)
                    case 6:
                        send_eth(account)
                    case 7:
                        get_estates(account)
                    case 8:
                        get_ad()
                    case 9:
                        print(f"Баланс вашего аккаунта: {w3.eth.get_balance(account)} ")
                    case 10:
                        get_balance(account)
                    case 11:
                        withdraw_to(account)
                    case 12:
                        account = ""
                        print("----------------------------")
                        print("> Вы вышли из аккаунта!")
                        print()
                    case _:
                        print()
                        print("Такой чиселки нету! Выберите от 1 до 12")
                        print()
            else:
                print()
                print("Введите цифру от 1 до 12")
                print()

if __name__ == "__main__":
    main()