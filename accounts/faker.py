from faker import Faker
from accounts.models import CustomUser

fake = Faker('ja_JP')
Faker.seed(313)

for i in range(5):
    name = 'test'+str(i)
    email = fake.safe_email()+str(i)
    password = fake.password()
    user = CustomUser(user_name=name, email=email, password=password)
    user.save()
