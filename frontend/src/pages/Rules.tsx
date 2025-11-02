import { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Stack,
  Tab,
  Tabs,
  Typography,
} from '@mui/material';
import AddTaskRoundedIcon from '@mui/icons-material/AddTaskRounded';
import AnalyticsRoundedIcon from '@mui/icons-material/AnalyticsRounded';

type RulesTab = 'definitions' | 'templates';

export default function RulesPage() {
  const [tab, setTab] = useState<RulesTab>('definitions');

  return (
    <Stack spacing={3}>
      <Card
        variant="outlined"
        sx={{ borderRadius: 3, overflow: 'hidden', boxShadow: '0 24px 60px rgba(15, 23, 42, 0.06)' }}
      >
        <Box sx={{ px: 3, pt: 3 }}>
          <Tabs
            value={tab}
            onChange={(_, value) => setTab(value)}
            textColor="primary"
            indicatorColor="primary"
            sx={{ '& .MuiTab-root': { textTransform: 'none', fontWeight: 600, minHeight: 48 } }}
          >
            <Tab
              value="definitions"
              icon={<AnalyticsRoundedIcon fontSize="small" />}
              iconPosition="start"
              label="Rule definitions"
            />
            <Tab
              value="templates"
              icon={<AddTaskRoundedIcon fontSize="small" />}
              iconPosition="start"
              label="Templates"
            />
          </Tabs>
        </Box>

        <Box sx={{ px: 3, pb: 3 }}>
          {tab === 'definitions' ? (
            <Stack spacing={3}>
              <Typography variant="subtitle1" color="text.secondary">
                Manage anomaly detection rules across businesses. Rules can be immediate, windowed, or aggregated.
              </Typography>
              <Card variant="outlined" sx={{ p: 3, borderRadius: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Coming soon
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 420 }}>
                  Rule authoring capabilities will appear here, including reusable presets, severity tagging, and simulation mode.
                </Typography>
              </Card>
            </Stack>
          ) : (
            <Stack spacing={3}>
              <Typography variant="subtitle1" color="text.secondary">
                Bootstrap new businesses with curated rule templates for common patterns.
              </Typography>
              <Box textAlign="center" sx={{ py: 6 }}>
                <Typography variant="body1" gutterBottom>
                  Template library is under construction.
                </Typography>
                <Button variant="contained" disableElevation startIcon={<AddTaskRoundedIcon />}>Notify me</Button>
              </Box>
            </Stack>
          )}
        </Box>
      </Card>
    </Stack>
  );
}
