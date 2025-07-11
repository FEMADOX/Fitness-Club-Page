// import { QueryClientProvider } from '@tanstack/react-query'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './presentation/App'
import './styles/index.css'
// import { queryClient } from './utils/globalErrorHandle'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    {/* <QueryClientProvider client={queryClient}> */}
      <App />
    {/* </QueryClientProvider> */}
  </React.StrictMode>
)
