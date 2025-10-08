import { Link, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./lib/auth";
import type { JSX } from "react";
import { Outlet } from "react-router-dom";
//pages
import Home from "./pages/Home";
import ViewReceipts from "./pages/ViewReceipts";
import ViewReceipt from "./pages/ViewReceipt";
import CreateReceipt from "./pages/CreateReceipt";

function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { isAuthed } = useAuth();
  return isAuthed ? <Outlet /> : <Navigate to="/Home" replace />;
  //return children;
}

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen flex flex-col">
        <main className="p-4 max-w-4xl w-full mx-auto">
          <Routes>
            <Route path="/Home" element={<Home />} />
            <Route element={<ProtectedRoute><></></ProtectedRoute>}>
              <Route path="/view-receipts" element={<ViewReceipts />} />
              <Route path="/receipt/:id" element={<ViewReceipt />} />
              <Route path="/create-receipt" element={<CreateReceipt />} />
            </Route>
            <Route path="*" element={<Navigate to="/Home" replace />} />
          </Routes>
        </main>
      </div>
    </AuthProvider>
  );
}
