import { Dumbbell } from "lucide-react";


const FooterSection = () => {
    return (
      <footer className="bg-gray-900 text-gray-300">
        <div className="container mx-auto px-4 py-12 md:py-16">
          <div className="grid md:grid-cols-4 gap-8 mb-12">
    
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <Dumbbell className="w-6 h-6 text-primary" />
                <span className="font-bold text-white text-lg">Fitness Club</span>
              </div>
              <p className="text-gray-400">
                A Modified Fitness Club that provide fitness & nutrition related
                solutions
              </p>
            </div>
  
      
            <div className="space-y-4">
              <h4 className="text-white font-semibold text-lg">About</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-primary transition">Programs</a></li>
                <li><a href="#" className="hover:text-primary transition">Nutrition</a></li>
                <li><a href="#" className="hover:text-primary transition">Pricing</a></li>
                <li><a href="#" className="hover:text-primary transition">Blog</a></li>
              </ul>
            </div>
  
         
            <div className="space-y-4">
              <h4 className="text-white font-semibold text-lg">Company</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-primary transition">About Us</a></li>
                <li><a href="#" className="hover:text-primary transition">Careers</a></li>
                <li><a href="#" className="hover:text-primary transition">Partners</a></li>
                <li><a href="#" className="hover:text-primary transition">Contact</a></li>
              </ul>
            </div>
  
    
            <div className="space-y-4">
              <h4 className="text-white font-semibold text-lg">Connect</h4>
              <div className="flex gap-4">
                <a href="#" className="p-2 hover:text-primary transition">
                    Instagram
                </a>
                <a href="#" className="p-2 hover:text-primary transition">
               Facebook
                </a>
                <a href="#" className="p-2 hover:text-primary transition">
                Twitter
                </a>
                <a href="#" className="p-2 hover:text-primary transition">
                Youtube
                </a>
              </div>
            </div>
          </div>
  
          <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
            <p>© 2024 Fitness Club. All rights reserved</p>
          </div>
        </div>
      </footer>
    );
  };
  
  export default FooterSection;