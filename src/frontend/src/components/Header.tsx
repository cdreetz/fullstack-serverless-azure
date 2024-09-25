import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const Header: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();

  return (
    <div className="p-2 mb-2">
      <Link to="/" className="text-lg font-semibold hover:text-blue-600 px-2">Home</Link>
      {isAuthenticated ? (
        <div className="flex gap-4 px-2">
          <Link to="/dashboard" className="text-lg font-semibold hover:text-blue-600">Dashboard</Link>
          <button onClick={logout} className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition-colors">
            Logout
          </button>
        </div>
      ) : (
        <Link to="/login" className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md transition-colors">
          Login
        </Link>
      )}
    </div>
  );
};

export default Header;
