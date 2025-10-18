import { instance } from "./api.config.js";



function login(email: string, password: string) {
    return instance.post("/api/Account/Login", JSON.stringify({ email: email, password: password }))
}

function refresh(accessToken: string, refreshToken: string) {
    return instance.post("/api/Account/Refresh", JSON.stringify({ accessToken: accessToken, refreshToken: refreshToken }));
}

function logout() {
    return instance.post("/api/Account/Logout");
}
function checkAuth(){
    return instance.get("/api/Account/CheckAuth");
}

const AuthService = {
    login,
    logout,
    refresh,
    checkAuth
}
export default AuthService