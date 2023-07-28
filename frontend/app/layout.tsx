/* Components */
import { Providers } from '@/lib/providers'
import MainMenu from './components/Menu'


export default function RootLayout({ children, }: { children: React.ReactNode }) {
  return (
    <Providers>
      <html lang="en">
        <body>
          <MainMenu />
          {children}
        </body>
      </html>
    </Providers>

  )
}
