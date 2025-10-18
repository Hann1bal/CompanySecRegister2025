import axios from "axios";

export const instance = axios.create({
  // к запросу будет приуепляться cookies
  withCredentials: true,
  baseURL: "http://localhost:5083",
});

//https://kb.ai-hippocrates.ru/kbapi
//https://localhost:5001
// создаем перехватчик запросов
// который к каждому запросу добавляет accessToken из localStorage
instance.interceptors.request.use((config) => {
  (config.headers.Authorization = `Bearer ${localStorage.getItem("token")}`),
    (config.headers["Content-Type"] = "application/json");
  return config;
});

// создаем перехватчик ответов
// который в случае невалидного accessToken попытается его обновить
// и переотправить запрос с обновленным accessToken
instance.interceptors.response.use(
  // в случае валидного accessToken ничего не делаем:
  (config) => {
    return config;
  }
);
