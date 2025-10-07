import { useAuth } from "../lib/auth";

export default function ViewReceipts() {
  const { logout } = useAuth();
  return (
    <div>
      <h1>Your Receipts</h1>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
