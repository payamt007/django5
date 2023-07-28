/* Components */
import { Providers } from '@/lib/providers'
import MainMenu from './components/Menu'
import { Anchor, Row, Col } from 'antd';
import StyledComponentsRegistry from '@/lib/AntdRegistry';

export default function RootLayout({ children, }: { children: React.ReactNode }) {
  return (
    <Providers>
      <html lang="en">
        <body>
          <StyledComponentsRegistry>
            <MainMenu />
            {children}
          </StyledComponentsRegistry>
        </body>
      </html>
    </Providers>

  )
}
