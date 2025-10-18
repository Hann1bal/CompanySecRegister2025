import { Routes, Route } from "react-router-dom";
import AuthPage from "../Pages/AuthPage";
import RegPage from "../Pages/RegPage";
import CompaniesListPage from "../Pages/CompanyList";
import CompanyInfo from "../Pages/CompanyInfo";
import IndustryGraph from "../Pages/IndustryGraph";
import CompanyAnalyticsPage from "../Pages/CompanyAnalysisPage";

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/reg" element={<RegPage />} />
      <Route path="/companies" element={<CompaniesListPage />} />
      <Route path="/company/:inn" element={<CompanyInfo/>} />
      <Route path="/graph" element={<IndustryGraph/>}/>
      <Route path="/analytics" element={<CompanyAnalyticsPage/>}/>
      <Route path="*" element={<AuthPage />} /> {/* fallback */}
    </Routes>
  );
};

export default AppRoutes;
