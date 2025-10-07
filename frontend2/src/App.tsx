import { Link, Navigate, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import ViewReceipts from "./pages/ViewReceipts";
import { AuthProvider, useAuth } from "./lib/auth";
import type { JSX } from "react";

function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { isAuthed } = useAuth();
  return isAuthed ? children : <Navigate to="/Home" replace />;
  //return children;
}

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen flex flex-col">
        <main className="p-4 max-w-4xl w-full mx-auto">
          <Routes>
            <Route path="/Home" element={<Home />} />
            <Route
              path="/receipts"
              element={
                <ProtectedRoute>
                  <ViewReceipts />
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
