import { Link, Navigate, Route, Routes } from "react-router-dom";
import Login from "./pages/Home";
import Receipts from "./pages/Receipts";
import ReceiptDetail from "./pages/ReceiptDetail";
import { AuthProvider, useAuth } from "./lib/auth";
import type { JSX } from "react";

function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { isAuthed } = useAuth();
  //return isAuthed ? children : <Navigate to="/Home" replace />;
  return children;
}

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen flex flex-col">
        <nav className="border-b px-4 py-3 flex items-center gap-4">
          <Link to="/receipts" className="font-medium">Receipts</Link>
        </nav>
        <main className="p-4 max-w-4xl w-full mx-auto">
          <Routes>
            <Route path="/Home" element={<Login />} />
            <Route
              path="/receipts"
              element={
                <ProtectedRoute>
                  <Receipts />
                </ProtectedRoute>
              }
            />
            <Route
              path="/receipts/:id"
              element={
                <ProtectedRoute>
                  <ReceiptDetail />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/Home" replace />} />
          </Routes>
        </main>
      </div>
    </AuthProvider>
  );
}
