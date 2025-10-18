import { Button, TextInput, Label, Card } from "flowbite-react";
import { useState } from "react";
import { Link } from "react-router-dom";

const AuthPage = () => {

    const [email, setEmail] = useState<string>("")
    const [password, setPassword] = useState<string>("")

    const onSumbit = () => {
        console.log('first', email, password)
    }

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <Card className="w-full max-w-md shadow-lg border border-gray-200">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
          Вход в систему
        </h1>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            onSumbit();
          }}
        >
          <div className="flex flex-col gap-4">
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
            <Link to="/companies">
              <Button type="submit" color="blue" className="w-full">
                Войти
              </Button>
            </Link>
            <Link to="/reg">
              <Button color="light" className="w-full">
                Нет аккаунта? Зарегистрироваться!
              </Button>
            </Link>
          </div>
        </form>
      </Card>
    </div>
  );
};

export default AuthPage;
