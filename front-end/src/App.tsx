import { ThemeProvider } from '@/context/theme-context'
import { Redirect, Route, Switch } from 'wouter'
import Navbar from './components/Navbar'
import FooterSection from './components/Footer'
import Register from './pages/Register'
import KnowMore from './pages/KnowMore'
import Login from './pages/Login'
import NotFound from './pages/NotFound'
import Index from './pages/Index'
import Logout from './components/Logout'
import { ProtectedRegistrationRoute, ProtectedRoute } from './components/ProtectedRoute'

function App() {
  const protectedRoute = (children: JSX.Element, url: string) => {
    return <ProtectedRoute url={url}>{children}</ProtectedRoute>
  }
  const authorizedNotAvailable = (children: JSX.Element) => {
    return <ProtectedRegistrationRoute url="/">{children}</ProtectedRegistrationRoute>
  }

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
        <Navbar />
        <Switch>
          <Route path="/" component={Index} />
          <Route path="/login" component={() => authorizedNotAvailable(<Login />)} />
          <Route path="/register" component={() => authorizedNotAvailable(<Register />)} />
          {/* <Route path="/logout" component={() => authorizedAvailable(<Logout />)} /> */}
          {/* <Route path="/know-more" component={() => authorizedAvailable(<KnowMore />)} /> */}
          <Route path="/logout" component={() => <Logout />} />
          <Route path="/know-more" component={() => protectedRoute(<KnowMore />, '/login')} />
          <Route component={NotFound} />
        </Switch>
        <FooterSection />
      </div>
    </ThemeProvider>
  )
}

export default App
