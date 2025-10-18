import { Button, TextInput, Label, Card } from "flowbite-react";
import { useState } from "react";
import { Link } from "react-router-dom";

const RegPage = () => {

  const [firstName, setFirstName] = useState<string>("")
  const [_, setsecondName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [passwordConfirm, setPasswordConfirm] = useState<string>("")

  const onSubmit = () => {
    console.log(
      "first",
      firstName,
      firstName,
      email,
      password,
      passwordConfirm
    );

  }
  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-blue-100 via-white to-green-100">
      <Card className="w-full max-w-md shadow-xl border border-gray-200 p-6">
        <h1 className="text-3xl font-extrabold text-center text-gray-800 mb-2">
          Регистрация
        </h1>
        <p className="text-center text-gray-500 mb-6">
          Создайте новый аккаунт, чтобы получить доступ к аналитике
        </p>

        <form
          className="flex flex-col gap-5"
          onSubmit={(e) => {
            e.preventDefault();
          }}
        >
          <div>
            <Label htmlFor="email" value="Фамилия" />
            <TextInput
              type="text"
              placeholder="Введите фамилию"
              required
              onChange={(e) => setFirstName(e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="email" value="Имя" />
            <TextInput
              type="text"
              placeholder="Введите имя"
              required
              onChange={(e) => setsecondName(e.target.value)}
            />
          </div>
          <div>
            <Label htmlFor="email" value="Email" />
            <TextInput
              id="email"
              type="email"
              placeholder="Введите email"
              required
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <Label htmlFor="password" value="Пароль" />
            <TextInput
              id="password"
              type="password"
              placeholder="Введите пароль"
              required
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div>
            <Label htmlFor="confirmPassword" value="Подтверждение пароль" />
            <TextInput
              id="confirmPassword"
              type="password"
              placeholder="Повторите пароль"
              required
              onChange={(e) => setPasswordConfirm(e.target.value)}
            />
          </div>

          <Button color="green" className="w-full text-lg font-semibold">
            Зарегистрироваться
          </Button>

          <div className="text-center">
            <span className="text-gray-600">Уже есть аккаунт?</span>{" "}
            <Link to="/auth">
              <Button color="light" className="w-full mt-2" onClick={onSubmit}>
                Войти в систему
              </Button>
            </Link>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default RegPage;
