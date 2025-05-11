import { ThemeProvider } from "@/context/theme-context";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Services from "./components/Services";
import ActiveSection from "./components/ActiveSection";
import Trainers from "./components/Trainers";
import Testimonials from "./components/Testimonials";
import SubscribeSection from "./components/SuscribeSection";
import FooterSection from "./components/Footer";

function App() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
        <Navbar />
        <main>
          <Hero />
          <Services />
          <ActiveSection />
          <Trainers />
          <Testimonials />
          <SubscribeSection />
        </main>
        <FooterSection />
      </div>
    </ThemeProvider>
  );
}

export default App;
