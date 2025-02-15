import { Menu } from "lucide-react";
import { X } from "lucide-react";
import { useState } from "react";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md z-20 border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <svg
              className="w-8 h-8 text-primary"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M4 12C4 7.58172 7.58172 4 12 4C16.4183 4 20 7.58172 20 12C20 16.4183 16.4183 20 12 20C7.58172 20 4 16.4183 4 12Z"
                stroke="currentColor"
                strokeWidth="2"
              />
              <path
                d="M15 9C15 10.6569 13.6569 12 12 12C10.3431 12 9 10.6569 9 9C9 7.34315 10.3431 6 12 6C13.6569 6 15 7.34315 15 9Z"
                fill="currentColor"
              />
            </svg>
            <span className="font-bold text-xl text-gray-900">
              Fitness Club
            </span>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            <a
              href="#"
              className="text-gray-600 hover:text-primary transition-colors"
            >
              Home
            </a>
            <a
              href="#training"
              className="text-gray-600 hover:text-primary transition-colors"
            >
              Training
            </a>
            <a
              href="#footer"
              className="text-gray-600 hover:text-primary transition-colors"
            >
              Contact
            </a>
          </div>

          {/* Mobile Menu Button */}
          <button className="md:hidden text-gray-600 hover:text-primary transition-colors">
           {isOpen ? <X size={24} className="z-40 relative" onClick={() => setIsOpen(false)} /> : <Menu className="z-40 relative" size={24} onClick={() => setIsOpen(true)} />}

            {isOpen && (
              <div className="fixed h-screen inset-0 top-0 bottom-0 z-10 bg-white/95 backdrop-blur-lg">
                <div className="absolute top-0 left-0 right-0 bottom-0 flex flex-col items-center justify-center">
                  <div className="w-full max-w-md px-4 py-4">
                    <div className="flex flex-col gap-4 ">
                      <a
                        href="#"
                        className="text-gray-800 font-bold hover:text-primary transition-colors"
                      >
                        Home
                      </a>
                      <a
                        href="#"
                        className="text-gray-800 font-bold hover:text-primary transition-colors"
                      >
                        Training
                      </a>
                      <a
                        href="#"
                        className="text-gray-800 font-bold hover:text-primary transition-colors"
                      >
                        Contact
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
