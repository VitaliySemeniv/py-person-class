class Person:
    # write your code here
    pass


def create_person_list(people: list) -> list:
    # write your code here
    pass
class Person:
    # Клас-атрибут: мапа "ім'я -> інстанс Person"
    people: dict[str, "Person"] = {}

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = int(age)
        # реєструємо кожен інстанс у словнику класу
        Person.people[name] = self

    def __repr__(self):
        # зручніше дебажити/дивитися
        return f"Person(name={self.name!r}, age={self.age!r})"


def create_person_list(people: list[dict]) -> list[Person]:
    """
    Приймає список словників (із ключами name, age, wife/husband)
    і повертає список інстансів Person.
    Якщо у словнику задано wife/husband != None — додає відповідний
    атрибут як посилання на інший інстанс Person.

    Важливо: якщо wife/husband == None — атрибут НЕ створюємо,
    щоб звернення person.wife підняло AttributeError (як у прикладі).
    """

    # 1) Спершу створюємо ВСІ інстанси (щоб посилання між ними були можливі)
    instances: list[Person] = []
    for p in people:
        name = p["name"]
        age = p["age"]
        instances.append(Person(name=name, age=age))

    # 2) Тепер проставляємо зв'язки (wife/husband), якщо вони задані
    for p in people:
        name = p["name"]
        person = Person.people[name]

        # Знаходимо, який "шлюбний" ключ присутній у словнику саме для цієї людини
        # (вхідні дані можуть містити 'wife' АБО 'husband', залежно від статі)
        spouse_key = None
        if "wife" in p:
            spouse_key = "wife"
        elif "husband" in p:
            spouse_key = "husband"

        if spouse_key is not None:
            spouse_name = p.get(spouse_key)
            if spouse_name is None:
                # Якщо None — пропускаємо, атрибут не створюємо
                continue

            # Перевіряємо, що така людина існує серед створених
            if spouse_name not in Person.people:
                raise ValueError(f"У даних вказано {spouse_key}={spouse_name}, "
                                 f"але такої особи немає у списку.")

            spouse_person = Person.people[spouse_name]
            # Додаємо атрибут дружини/чоловіка як посилання на інстанс
            setattr(person, spouse_key, spouse_person)

    return instances
