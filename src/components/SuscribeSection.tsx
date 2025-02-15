import { Mail, Dumbbell } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const SubscribeSection = () => {
  return (
    <section className="relative py-16 md:py-24 bg-gradient-to-b from-primary/10 to-white">
      <div className="container mx-auto px-4">
        <div className="max-w-2xl mx-auto text-center">
          <div className="space-y-6 mb-12">
            <Dumbbell className="w-12 h-12 text-primary mx-auto" />
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900">
              Subscribe Our Fitness Articles
            </h2>
            <p className="text-gray-600 text-lg max-w-md mx-auto">
              Physical activity is defined as any bodily movement produced by
              skeletal muscles that results in energy expenditure
            </p>
          </div>

          <form className="flex flex-col md:flex-row gap-4 max-w-lg mx-auto">
            <div className="relative flex-1">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <Input
                placeholder="Type Your Email Address"
                className="pl-10 py-6 text-base"
              />
            </div>
            <Button className="py-6 px-8 text-base bg-primary hover:bg-primary/90">
              Subscribe
            </Button>
          </form>

      
          <div className="absolute left-4 top-8 -rotate-12 text-primary/10 font-bold text-2xl">
            G3 3 x279
          </div>
          <div className="absolute right-8 bottom-12 text-primary/5 font-black text-4xl">
            FITNESS
          </div>
        </div>
      </div>
    </section>
  );
};

export default SubscribeSection;