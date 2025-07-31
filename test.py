from pydantic import BaseModel


class MyModel(BaseModel):
    created: int = 3.4
    desc: str = "test"


m = MyModel()
print(m.model_dump())

n = MyModel(created=2.5, desc="description")
print(n.model_dump())
