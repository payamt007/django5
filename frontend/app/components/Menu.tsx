import {
  AppstoreOutlined,
  CalendarOutlined,
  LinkOutlined,
  MailOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import { Divider, Menu, Switch } from 'antd';
import type { MenuProps, MenuTheme } from 'antd/es/menu';
import Link from 'next/link'
type MenuItem = Required<MenuProps>['items'][number];

function getItem(
  label: React.ReactNode,
  key?: React.Key | null,
  icon?: React.ReactNode,
  children?: MenuItem[],
): MenuItem {
  return {
    key,
    icon,
    children,
    label,
  } as MenuItem;
}

const items: MenuItem[] = [
  getItem(
    <Link  href="/">
      Home
    </Link >,
    'link-0',
    <LinkOutlined />,
  ),
  getItem(
    <Link  href="/feeds">
      Feeds
    </Link>,
    'link-1',
    <LinkOutlined />,
  ),
  
];

const MainMenu: React.FC = () => {
  return (
    <>
      <Divider type="vertical" />
      <br />
      <br />
      <Menu
        style={{ width: 256 }}
        defaultSelectedKeys={['1']}
        defaultOpenKeys={['sub1']}
        items={items}
      />
    </>
  );
};

export default MainMenu;
