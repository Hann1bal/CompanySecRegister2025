import { Routes, Route } from "react-router-dom";
import AuthPage from "../Pages/AuthPage";
import RegPage from "../Pages/RegPage";
import CompaniesListPage from "../Pages/CompanyList";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/reg" element={<RegPage />} />
      <Route path="/companies" element={<CompaniesListPage />} />
      <Route path="*" element={<AuthPage />} /> {/* fallback */}
    </Routes>
  );
};

export default AppRoutes;
