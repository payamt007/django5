/* Components */
import { Providers } from '@/lib/providers'
import MainMenu from './components/Menu'
import { Row, Col } from 'antd';
import StyledComponentsRegistry from '@/lib/AntdRegistry';

export default function RootLayout({ children, }: { children: React.ReactNode }) {
  return (
    <Providers>
      <StyledComponentsRegistry>
        <html lang="en">
          <body>
            {children}
            {/* <Row>
              <Col span={6}><MainMenu /></Col>
              <Col span={18}>{children}</Col>
            </Row> */}
          </body>
        </html>
      </StyledComponentsRegistry>
    </Providers>
  )
}
