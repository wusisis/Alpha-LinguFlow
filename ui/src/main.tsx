import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter } from 'react-router-dom'
import { MantineProvider } from '@mantine/core'
import { Notifications } from '@mantine/notifications'
import { ErrorBoundary } from 'react-error-boundary'
import { ModalsProvider } from '@mantine/modals'
import { QueryClient, QueryClientProvider } from 'react-query'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { AppRoutes } from './routes.tsx'

dayjs.extend(relativeTime)

import '@mantine/core/styles.css'
import '@mantine/notifications/styles.css'
import { CustomError } from './components/ErrorBoundary.tsx'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: false
    }
  }
})

ReactDOM.cr