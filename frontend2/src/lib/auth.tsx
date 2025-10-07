import React from "react";

interface AuthContextShape {
  isAuthed: boolean;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = React.createContext<AuthContextShape | undefined>(
  undefined
);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = React.useState<string | null>(
    () => localStorage.getItem("token")
  );

  const login = (t: string) => {
    setToken(t);
    localStorage.setItem("token", t);
  };
  const logout = () => {
    setToken(null);
    localStorage.removeItem("token");
  };

  const value: AuthContextShape = {
    isAuthed: Boolean(token),
    token,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = React.useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
