

const trainers = [
  {
    name: "Jason Holder",
    role: "Fitness Expert",
  
  },
  {
    name: "Sarah Johnson",
    role: "Yoga Instructor",
  },
  {
    name: "Michael Brown",
    role: "Nutrition Coach",
  }
];

const Trainers = () => {
  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <p className="text-primary font-medium mb-4">Our Instructors</p>
          <h2 className="text-4xl font-bold mb-4">
            Meet Our Extremely<br />Talented Trainers
          </h2>
        </div>
        
        <div className="grid mx-auto place-content-center grid-cols-1 gap-8">
          <img
            className="mx-auto rounded-2xl"
           
             src="/Image3.png"
             alt="Our Trainers"
    
           />
        </div>
        <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-20">
          {trainers.map((trainer, index) => (
            <li key={index} className="flex flex-col mt-6 items-center">
              {trainer.name} - {trainer.role}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
};

export default Trainers;
