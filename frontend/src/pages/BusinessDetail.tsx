import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Grid,
  Skeleton,
  Snackbar,
  Stack,
  Tab,
  Tabs,
  TextField,
  Typography,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import DashboardRoundedIcon from '@mui/icons-material/DashboardRounded';
import SchemaRoundedIcon from '@mui/icons-material/SchemaRounded';
import {
  addField,
  getBusiness,
  listFields,
  updateBusiness,
  BusinessDefinition,
  FieldDefinition,
  FieldDefinitionCreate,
} from '../api/client';
import FieldCreateDialog from '../components/FieldCreateDialog';

type DetailTab = 'overview' | 'schema';

export default function BusinessDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [business, setBusiness] = useState<BusinessDefinition | null>(null);
  const [fields, setFields] = useState<FieldDefinition[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [edit, setEdit] = useState({ name: '', description: '' });
  const [saving, setSaving] = useState(false);
  const [openAddField, setOpenAddField] = useState(false);
  const [snack, setSnack] = useState<string | null>(null);
  const [tab, setTab] = useState<DetailTab>('overview');

  async function refresh() {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const [definition, schema] = await Promise.all([getBusiness(id), listFields(id)]);
      setBusiness(definition);
      setEdit({ name: definition.name, description: definition.description || '' });
      setFields(schema);
    } catch (err: any) {
      setError(err?.message || 'Failed to load business');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, [id]);

  async function onSave() {
    if (!id) return;
    setSaving(true);
    try {
      const updated = await updateBusiness(id, {
        name: edit.name.trim() || undefined,
        description: edit.description.trim() || undefined,
      });
      setBusiness(updated);
      setSnack('Business updated');
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to save changes');
    } finally {
      setSaving(false);
    }
  }

  async function onCreateField(payload: FieldDefinitionCreate) {
    if (!id) return;
    try {
      await addField(id, payload);
      setOpenAddField(false);
      setSnack('Field created');
      const schema = await listFields(id);
      setFields(schema);
      setTab('schema');
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to add field');
    }
  }

  return (
    <Stack spacing={3}>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/businesses')}>
          Back to catalogue
        </Button>
        {business && (
          <Typography variant="h6" fontWeight={600} color="text.secondary">
            {business.name}
          </Typography>
        )}
      </Box>

      {error && <Alert severity="error">{error}</Alert>}

      <Card variant="outlined" className="square-card">
        <Box sx={{ px: 3, pt: 3 }}>
          <Tabs
            value={tab}
            onChange={(_, value) => setTab(value)}
            textColor="primary"
            indicatorColor="primary"
            sx={{ '& .MuiTab-root': { textTransform: 'none', fontWeight: 600, minHeight: 48 } }}
          >
            <Tab value="overview" icon={<DashboardRoundedIcon fontSize="small" />} iconPosition="start" label="Overview" />
            <Tab value="schema" icon={<SchemaRoundedIcon fontSize="small" />} iconPosition="start" label="Schema" />
          </Tabs>
        </Box>

        <Box sx={{ px: 3, pb: 3 }}>
          {tab === 'overview' ? (
            loading || !business ? (
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Skeleton height={56} />
                </Grid>
                <Grid item xs={12} md={6}>
                  <Skeleton height={56} />
                </Grid>
                <Grid item xs={12} md={2}>
                  <Skeleton height={40} />
                </Grid>
              </Grid>
            ) : (
              <Stack spacing={3}>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs={12} md={4}>
                    <TextField
                      label="Name"
                      value={edit.name}
                      onChange={(event) => setEdit((prev) => ({ ...prev, name: event.target.value }))}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      label="Description"
                      value={edit.description}
                      onChange={(event) => setEdit((prev) => ({ ...prev, description: event.target.value }))}
                      fullWidth
                    />
                  </Grid>
                  <Grid item xs={12} md={2}>
                    <Button onClick={onSave} variant="contained" fullWidth disabled={saving}>
                      Save
                    </Button>
                  </Grid>
                </Grid>
                <Typography variant="caption" color="text.secondary">
                  Created: {new Date(business.created_at).toLocaleString()}
                </Typography>
                <Card variant="outlined" className="square-card" sx={{ p: 2, backgroundColor: '#f8fafc' }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Next steps
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Use the Schema tab to define fields, then add rules to detect anomalies across incoming events.
                  </Typography>
                </Card>
              </Stack>
            )
          ) : (
            <Stack spacing={3}>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Typography variant="subtitle1">Schema fields</Typography>
                <Button startIcon={<AddIcon />} variant="contained" onClick={() => setOpenAddField(true)}>
                  Add field
                </Button>
              </Box>
              {loading ? (
                <Stack spacing={1}>
                  <Skeleton height={48} />
                  <Skeleton height={48} />
                  <Skeleton height={48} />
                </Stack>
              ) : fields.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No fields yet. Use "Add field" to describe the data structure for this business.
                </Typography>
              ) : (
                <Grid container spacing={2}>
                  {fields.map((field) => (
                    <Grid item xs={12} md={6} lg={4} key={field.id}>
                      <Card variant="outlined" className="square-card" sx={{ height: '100%' }}>
                        <CardContent>
                          <Stack spacing={1}>
                            <Typography variant="subtitle1">{field.name}</Typography>
                            <Stack direction="row" spacing={1}>
                              <Chip size="small" label={field.data_type} color="primary" variant="outlined" />
                              {field.required && <Chip size="small" label="required" color="warning" />}
                            </Stack>
                            <Typography variant="body2" color="text.secondary">
                              {field.description || "No description provided."}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              Created: {new Date(field.created_at).toLocaleString()}
                            </Typography>
                          </Stack>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              )}
            </Stack>
          )}
        </Box>
      </Card>

      <FieldCreateDialog open={openAddField} onClose={() => setOpenAddField(false)} onSubmit={onCreateField} />
      <Snackbar open={!!snack} autoHideDuration={2400} onClose={() => setSnack(null)} message={snack ?? ''} />
    </Stack>
  );
}


