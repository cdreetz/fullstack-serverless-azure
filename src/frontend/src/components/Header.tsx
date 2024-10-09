import React from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { Button } from "./ui/button";
import { Menu } from "lucide-react";
import { useTheme } from "../contexts/ThemeContext";
import { Moon, Sun } from "lucide-react";

const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={toggleTheme}
      aria-label="Toggle theme"
    >
      {theme === "dark" ? <Sun className="h-[1.2rem] w-[1.2rem]" /> : <Moon className="h-[1.2rem] w-[1.2rem]" />}
    </Button>
  );
};

const Header: React.FC = () => {
  const { isAuthenticated, logout } = useAuth();
  return (
    <div className="p-2 mb-2 flex justify-between items-center">
      <Link to="/" className="text-lg font-semibold hover:text-blue-600">
        Tools
      </Link>
      <div className="relative">
        <ThemeToggle />
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" size="icon">
              <Menu className="h-[1.2rem] w-[1.2rem]" />
              <span className="sr-only">Toggle menu</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem>
              <Link to="/" className="w-full">Home</Link>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Link to="/summary" className="w-full">Summary</Link>
            </DropdownMenuItem>
            {isAuthenticated ? (
              <>
                <DropdownMenuItem>
                  <Link to="/dashboard" className="w-full">Dashboard</Link>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <button onClick={logout} className="w-full text-left text-red-500 hover:text-red-600">
                    Logout
                  </button>
                </DropdownMenuItem>
              </>
            ) : (
              <DropdownMenuItem>
                <Link to="/login" className="w-full">Login</Link>
              </DropdownMenuItem>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  );
};

export default Header;
