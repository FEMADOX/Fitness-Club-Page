
import { useIsMobile } from "@/hooks/use-mobile";

const Hero = () => {
  const isMobile = useIsMobile();

  return (
    <section className="relative min-h-screen bg-white overflow-hidden">
      <div className="container mx-auto px-4 pt-32 pb-20">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div className="relative z-10 animate-fadeIn">
            <p className="text-primary font-medium mb-4">Fitness Club</p>
            <h1 className="text-5xl md:text-6xl font-bold mb-6 hero-text-gradient">
              Sweat, Smile
              <br />
              And Repeat
            </h1>
            <p className="text-gray-600 mb-8 max-w-md">
              A gym is a club, building, or large room, usually containing special equipment, where people go to exercise and get fit.
            </p>
            <div className="flex flex-wrap gap-4">
              <button className="btn-primary">
                Join Now
              </button>
              <button className="btn-secondary">
                Know More
              </button>
            </div>
          </div>
          
          <div className={`relative z-10 animate-fadeIn ${isMobile ? 'mt-8' : ''}`}>
            <div className="relative w-full max-w-md mx-auto">
              <img
                src="/Image1.png"
                alt="Fitness"
                className="w-full h-full object-cover rounded-2xl shadow-lg"
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
