import { useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Button,
  Card,
  Stack,
  Tab,
  Tabs,
  Typography,
} from '@mui/material';
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';
import PlaylistAddCheckRoundedIcon from '@mui/icons-material/PlaylistAddCheckRounded';
import LaunchIcon from '@mui/icons-material/Launch';
import { useNavigate } from 'react-router-dom';
import { BusinessDefinition, BusinessCreate, createBusiness, listBusinesses } from '../api/client';
import BusinessCreateDialog from '../components/BusinessCreateDialog';

export default function BusinessesPage() {
  const navigate = useNavigate();
  const [items, setItems] = useState<BusinessDefinition[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [openCreate, setOpenCreate] = useState(false);
  const [tab, setTab] = useState<'list' | 'create'>('list');

  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      const data = await listBusinesses();
      setItems(data);
    } catch (err: any) {
      setError(err?.message ?? 'Failed to load businesses');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleCreate(payload: BusinessCreate) {
    try {
      const created = await createBusiness(payload);
      setItems((prev) => [created, ...prev]);
      setError(null);
      setTab('list');
      navigate(`/businesses/${created.id}`);
    } catch (err: any) {
      const message = err?.response?.data?.detail || err?.message || 'Failed to create business';
      setError(message);
      throw new Error(message);
    }
  }

  return (
    <Stack spacing={3}>
      <Box>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            borderBottom: '1px solid #dfe3e8',
          }}
        >
          <Tabs
            value={tab}
            onChange={(_, value) => setTab(value)}
            aria-label="Business workspace tabs"
            textColor="primary"
            indicatorColor="primary"
            sx={{
              '& .MuiTab-root': {
                textTransform: 'none',
                alignItems: 'center',
                fontWeight: 600,
                minHeight: 42,
                mr: 3,
              },
            }}
          >
            <Tab value="list" icon={<PlaylistAddCheckRoundedIcon fontSize="small" />} iconPosition="start" label="Catalogue" />
            <Tab value="create" icon={<AddCircleOutlineRoundedIcon fontSize="small" />} iconPosition="start" label="Create new" />
          </Tabs>
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          Create and manage the business use cases the anomaly engine should monitor. Each business can own its own schema and rules.
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {tab === 'list' ? (
        <Stack spacing={2}>
          <Typography variant="subtitle1" color="text.secondary">
            Browse all defined businesses and drill into their schema, rules, and activity.
          </Typography>
          {loading ? (
            <Typography variant="body2" color="text.secondary">
              Loading...
            </Typography>
          ) : items.length === 0 ? (
            <Typography variant="body2" color="text.secondary">
              No businesses yet. Switch to "Create new" to add your first business definition.
            </Typography>
          ) : (
            <Stack spacing={2}>
              {items.map((business) => (
                <Card key={business.id} variant="outlined" className="square-card" sx={{ p: 2, display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="subtitle1" fontWeight={600} noWrap>
                      {business.name}
                    </Typography>
                    <Button
                      size="small"
                      endIcon={<LaunchIcon fontSize="small" />}
                      onClick={() => navigate(`/businesses/${business.id}`)}
                    >
                      Open workspace
                    </Button>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {business.description || 'No description provided.'}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Created: {new Date(business.created_at).toLocaleString()}
                  </Typography>
                </Card>
              ))}
            </Stack>
          )}
        </Stack>
      ) : (
        <Stack spacing={3}>
          <Typography variant="subtitle1" color="text.secondary">
            Provide a name and optional description - fields and rules can be defined later from the business workspace.
          </Typography>
          <Card variant="outlined" className="square-card" sx={{ p: 4, textAlign: 'center', backgroundColor: '#f8fafc', borderStyle: 'dashed', borderColor: 'rgba(0, 102, 204, 0.3)' }}>
            <Typography variant="h6" gutterBottom>
              Launch the create wizard
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 420, mx: 'auto', mb: 3 }}>
              The guided wizard captures the minimum information to start tracking a new business case. You can enrich it afterwards with schema fields, rules, and view configuration.
            </Typography>
            <Button
              variant="contained"
              size="large"
              startIcon={<AddCircleOutlineRoundedIcon />}
              disableElevation
              onClick={() => setOpenCreate(true)}
            >
              New business
            </Button>
          </Card>
        </Stack>
      )}

      <BusinessCreateDialog open={openCreate} onClose={() => setOpenCreate(false)} onSubmit={handleCreate} />
    </Stack>
  );
}



