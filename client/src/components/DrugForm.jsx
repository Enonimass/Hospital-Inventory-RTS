import { useState } from 'react';
import { TextField, Button, Stack } from '@mui/material';
import api from '../services/api';

export default function DrugForm() {
  const [formData, setFormData] = useState({ name: '', quantity: 0, threshold: 5 });

  const handleSubmit = (e) => {
    e.preventDefault();
    api.post('/drugs', formData).then(() => alert('Drug added!'));
  };

  return (
    <form onSubmit={handleSubmit}>
      <Stack spacing={2}>
        <TextField label="Drug Name" required onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
        <TextField label="Quantity" type="number" onChange={(e) => setFormData({ ...formData, quantity: e.target.value })} />
        <TextField label="Alert Threshold" type="number" onChange={(e) => setFormData({ ...formData, threshold: e.target.value })} />
        <Button variant="contained" type="submit">Save</Button>
      </Stack>
    </form>
  );
}