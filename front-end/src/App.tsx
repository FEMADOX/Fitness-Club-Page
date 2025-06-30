import { ThemeProvider } from '@/context/theme-context'
import { Route, Switch } from 'wouter'
import Navbar from './components/Navbar'
import FooterSection from './components/Footer'
import Register from './pages/Register'
import KnowMore from './pages/KnowMore'
import Login from './pages/Login'
import NotFound from './pages/NotFound'
import Index from './pages/Index'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
        <Navbar />
        <Switch>
          <Route path="/" component={Index} />
          <Route
            path="/know-more"
            component={() => (
              <ProtectedRoute>
                <KnowMore />
              </ProtectedRoute>
            )}
          />
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />
          <Route component={NotFound} />
        </Switch>
        <FooterSection />
      </div>
    </ThemeProvider>
  )
}

export default App
