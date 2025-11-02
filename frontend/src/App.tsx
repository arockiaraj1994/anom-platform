import {
  Box,
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  Tooltip,
  Typography,
} from '@mui/material';
import { NavLink, Navigate, Route, Routes, useLocation } from 'react-router-dom';
import BusinessPage from './pages/Businesses';
import BusinessDetailPage from './pages/BusinessDetail';
import RulesPage from './pages/Rules';
import BusinessCenterRoundedIcon from '@mui/icons-material/BusinessCenterRounded';
import RuleRoundedIcon from '@mui/icons-material/RuleRounded';
import SettingsRoundedIcon from '@mui/icons-material/SettingsRounded';
import MenuOpenRoundedIcon from '@mui/icons-material/MenuOpenRounded';

const navItems = [
  { to: '/businesses', label: 'Businesses', icon: <BusinessCenterRoundedIcon /> },
  { to: '/rules', label: 'Rules', icon: <RuleRoundedIcon /> },
];

function Sidebar() {
  const location = useLocation();

  return (
    <Box component="nav" className="app-sidebar">
      <Box className="pf-avatar">AP</Box>
      <Divider flexItem sx={{ borderColor: 'rgba(148, 163, 184, 0.2)', width: '100%' }} />
      <List sx={{ width: '100%', px: 1, flexGrow: 1 }}>
        {navItems.map((item) => {
          const active = location.pathname.startsWith(item.to);
          return (
            <ListItem key={item.to} disablePadding sx={{ mb: 1 }}>
              <Tooltip title={item.label} placement="right">
                <ListItemButton
                  component={NavLink}
                  to={item.to}
                  sx={{
                    minHeight: 60,
                    justifyContent: 'center',
                    borderLeft: active ? '3px solid #2491ff' : '3px solid transparent',
                    backgroundColor: active ? 'rgba(36, 145, 255, 0.12)' : 'transparent',
                    borderRadius: 0,
                  }}
                >
                  <ListItemIcon sx={{ color: active ? '#60a5fa' : 'rgba(255,255,255,0.7)', minWidth: 0 }}>
                    {item.icon}
                  </ListItemIcon>
                </ListItemButton>
              </Tooltip>
            </ListItem>
          );
        })}
      </List>

      <ListItem disablePadding>
        <Tooltip title="Settings" placement="right">
          <IconButton sx={{ color: 'rgba(255,255,255,0.7)' }}>
            <SettingsRoundedIcon />
          </IconButton>
        </Tooltip>
      </ListItem>
    </Box>
  );
}

function Header() {
  const location = useLocation();
  const active = navItems.find((item) => location.pathname.startsWith(item.to));
  const title = active?.label ?? 'Dashboard';

  return (
    <Box component="header" className="app-header">
      <Box>
        <Typography variant="h5" gutterBottom sx={{ mb: 0 }}>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Anom Platform · Unified anomaly intelligence workspace
        </Typography>
      </Box>
      <IconButton sx={{ color: 'text.secondary' }}>
        <MenuOpenRoundedIcon />
      </IconButton>
    </Box>
  );
}

export default function App() {
  return (
    <Box className="app-shell">
      <Sidebar />
      <Box className="app-main">
        <Header />
        <Box component="main" className="app-content">
          <Routes>
            <Route path="/" element={<Navigate to="/businesses" replace />} />
            <Route path="/businesses" element={<BusinessPage />} />
            <Route path="/businesses/:id" element={<BusinessDetailPage />} />
            <Route path="/rules" element={<RulesPage />} />
          </Routes>
        </Box>
      </Box>
    </Box>
  );
}
