import Link from '@mui/material/Link';
import Box from '@mui/material/Box';

const preventDefault = (event: React.SyntheticEvent) => event.preventDefault();


export default function Links() {
  return (
    <Box
      sx={{
        typography: 'body1',
        '& > :not(style) ~ :not(style)': {
          ml: 2,
        },
      }}
    >
      <Link href="/">Home</Link>
      <Link href="/feeds/">Feeds</Link>
      <Link href="#" variant="body2">
        {'variant="body2"'}
      </Link>
    </Box>
  );
}