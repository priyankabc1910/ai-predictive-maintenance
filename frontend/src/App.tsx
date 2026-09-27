import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppShell } from "./components/layout/AppShell";
import Overview from "./pages/Overview";
import Fleet from "./pages/Fleet";
import RULPredictions from "./pages/RULPredictions";
import Anomalies from "./pages/Anomalies";
import Maintenance from "./pages/Maintenance";
import Intelligence from "./pages/Intelligence";
import Reports from "./pages/Reports";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<Overview />} />
          <Route path="fleet" element={<Fleet />} />
          <Route path="rul" element={<RULPredictions />} />
          <Route path="anomalies" element={<Anomalies />} />
          <Route path="maintenance" element={<Maintenance />} />
          <Route path="intelligence" element={<Intelligence />} />
          <Route path="reports" element={<Reports />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
