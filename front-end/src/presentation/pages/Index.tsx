import Hero from '@/presentation/components/Hero'
import Services from '@/presentation/components/Services'
import ActiveSection from '@/presentation/components/ActiveSection'
import Trainers from '@/presentation/components/Trainers'
import Testimonials from '@/presentation/components/Testimonials'
import SuscribeSection from '@/presentation/components/SubcribeSection'

const Index = () => {
  return (
    <main className="min-h-screen bg-white">
      <Hero />
      <Services />
      <ActiveSection />
      <Trainers />
      <Testimonials />
      <SuscribeSection />
    </main>
  )
}

export default Index
