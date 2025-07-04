import {
  FooterSection,
  Logout,
  Navbar,
  ProtectedRegistrationRoute,
  ProtectedRoute,
  RegistrationForm
} from '@/components'
import { ThemeProvider } from '@/context/theme-context'
import { Index, KnowMore, NotFound } from '@/pages'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner'
import { Route, Switch } from 'wouter'
import { LOGIN_URL, REGISTER_URL } from './api/constants'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 10, // 10 minutes
      retry: 3,
      refetchOnWindowFocus: false
    },
    mutations: {
      retry: 3
    }
  }
})

function App() {
  const protectedRoute = (children: JSX.Element, url: string) => {
    return <ProtectedRoute url={url}>{children}</ProtectedRoute>
  }
  const authorizedNotAvailable = (children: JSX.Element) => {
    return <ProtectedRegistrationRoute url="/">{children}</ProtectedRegistrationRoute>
  }

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors">
          <Navbar />
          <Switch>
            <Route path="/" component={Index} />
            <Route
              path="/login"
              component={() =>
                authorizedNotAvailable(<RegistrationForm registerUrl="/login" />)
              }
            />
            <Route
              path="/register"
              component={() =>
                authorizedNotAvailable(
                  <RegistrationForm registerUrl="/register" />
                )
              }
            />
            <Route path="/logout" component={() => <Logout />} />
            <Route path="/know-more" component={() => protectedRoute(<KnowMore />, '/login')} />
            <Route component={NotFound} />
          </Switch>
          <FooterSection />
          <Toaster
            position="bottom-right"
            richColors
            closeButton
            toastOptions={{
              duration: 10000
            }}
          />
        </div>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App
