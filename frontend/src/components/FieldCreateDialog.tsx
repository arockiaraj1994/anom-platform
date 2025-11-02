import { useEffect, useMemo, useState } from 'react';
import {
  Box,
  Button,
  Checkbox,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  FormControlLabel,
  IconButton,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import SchemaIcon from '@mui/icons-material/Schema';
import CheckCircleRoundedIcon from '@mui/icons-material/CheckCircleRounded';
import { FieldDefinitionCreate, FieldDataType } from '../api/client';

const TYPES: { value: FieldDataType; label: string }[] = [
  { value: 'string', label: 'String' },
  { value: 'integer', label: 'Integer' },
  { value: 'float', label: 'Float' },
  { value: 'boolean', label: 'Boolean' },
  { value: 'datetime', label: 'Datetime' },
];

interface FieldCreateDialogProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (payload: FieldDefinitionCreate) => Promise<void> | void;
}

export default function FieldCreateDialog({ open, onClose, onSubmit }: FieldCreateDialogProps) {
  const [form, setForm] = useState<FieldDefinitionCreate>({ name: '', data_type: 'string', required: true, description: '' });
  const [submitting, setSubmitting] = useState(false);
  const [nameTouched, setNameTouched] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) {
      resetForm();
    }
  }, [open]);

  function resetForm() {
    setForm({ name: '', data_type: 'string', required: true, description: '' });
    setNameTouched(false);
    setSubmitError(null);
  }

  const nameValue = form.name;
  const descriptionValue = form.description ?? '';
  const nameValid = useMemo(() => nameValue.trim().length > 0, [nameValue]);
  const nameHelper = nameTouched && !nameValid ? 'Please provide a field name.' : `${nameValue.length}/120 characters`;
  const descriptionHelper = `${descriptionValue.length}/500 characters`;

  const closeDialog = () => {
    if (submitting) return;
    resetForm();
    onClose();
  };

  async function handleSubmit() {
    setNameTouched(true);
    if (!nameValid) return;
    setSubmitting(true);
    setSubmitError(null);
    try {
      await onSubmit({
        ...form,
        name: nameValue.trim(),
        description: descriptionValue.trim() ? descriptionValue.trim() : undefined,
      });
      closeDialog();
    } catch (error: any) {
      const message = error?.message || 'Unable to create field. Please try again.';
      setSubmitError(message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Dialog
      open={open}
      onClose={(_, reason) => {
        if (reason === 'backdropClick' && submitting) return;
        closeDialog();
      }}
      fullWidth
      maxWidth="sm"
      PaperProps={{
        sx: {
          borderRadius: 4,
          boxShadow: '0 32px 80px rgba(15, 23, 42, 0.25)',
          overflow: 'hidden',
          background: 'linear-gradient(180deg, #ffffff 0%, #f7f9fc 100%)',
        },
      }}
    >
      <DialogTitle sx={{ px: 4, pt: 4, pb: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Box
          sx={{
            width: 48,
            height: 48,
            borderRadius: 3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            bgcolor: 'secondary.main',
            color: 'secondary.contrastText',
            boxShadow: '0 12px 24px rgba(107, 114, 128, 0.35)',
          }}
        >
          <SchemaIcon fontSize="medium" />
        </Box>
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h6" fontWeight={600} gutterBottom>
            New Field
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Describe the schema attribute and how the rule engine should interpret it.
          </Typography>
        </Box>
        <IconButton onClick={closeDialog} size="small" sx={{ color: 'text.secondary' }}>
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <Divider sx={{ mx: 4 }} />

      <DialogContent sx={{ px: 4, pt: 3, pb: 1 }}>
        <Stack spacing={3}>
          <TextField
            label="Field name"
            placeholder="e.g. durationMs"
            value={nameValue}
            onChange={(event) => setForm((previous) => ({ ...previous, name: event.target.value }))}
            onBlur={() => setNameTouched(true)}
            required
            error={nameTouched && !nameValid}
            helperText={nameHelper}
            inputProps={{ maxLength: 120 }}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                backgroundColor: '#fff',
                '& fieldset': {
                  borderColor: 'rgba(148, 163, 184, 0.4)',
                },
                '&:hover fieldset': {
                  borderColor: 'secondary.light',
                },
                '&.Mui-focused fieldset': {
                  borderColor: 'secondary.main',
                  borderWidth: 2,
                },
              },
            }}
          />

          <TextField
            select
            label="Data type"
            value={form.data_type}
            onChange={(event) => setForm((previous) => ({ ...previous, data_type: event.target.value as FieldDataType }))}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                backgroundColor: '#fff',
              },
            }}
          >
            {TYPES.map((type) => (
              <MenuItem key={type.value} value={type.value}>
                {type.label}
              </MenuItem>
            ))}
          </TextField>

          <FormControlLabel
            control={
              <Checkbox
                checked={form.required}
                onChange={(event) => setForm((previous) => ({ ...previous, required: event.target.checked }))}
              />
            }
            label="Required"
          />

          <TextField
            label="Description"
            placeholder="How will this field be used?"
            value={descriptionValue}
            onChange={(event) => setForm((previous) => ({ ...previous, description: event.target.value }))}
            multiline
            minRows={2}
            inputProps={{ maxLength: 500 }}
            helperText={descriptionHelper}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                backgroundColor: '#fff',
              },
            }}
          />

          {submitError && (
            <Box
              sx={{
                px: 2,
                py: 1.5,
                borderRadius: 2,
                bgcolor: 'rgba(244, 67, 54, 0.08)',
                color: 'error.main',
                border: '1px solid rgba(244, 67, 54, 0.2)',
              }}
            >
              <Typography variant="body2">{submitError}</Typography>
            </Box>
          )}
        </Stack>
      </DialogContent>

      <DialogActions
        sx={{
          px: 4,
          py: 3,
          bgcolor: 'rgba(15, 23, 42, 0.02)',
          borderTop: (theme) => `1px solid ${theme.palette.divider}`,
        }}
      >
        <Button onClick={closeDialog} color="inherit" sx={{ fontWeight: 600 }} disabled={submitting}>
          Cancel
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disableElevation
          startIcon={submitting ? <CircularProgress size={16} color="inherit" /> : <CheckCircleRoundedIcon fontSize="small" />}
          disabled={submitting || !nameValid}
          sx={{ px: 3, fontWeight: 600 }}
        >
          {submitting ? 'Creating…' : 'Create field'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
