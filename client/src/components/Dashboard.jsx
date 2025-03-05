import { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import api from '../services/api';

export default function Dashboard() {
  const [drugs, setDrugs] = useState([]);

  useEffect(() => {
    api.get('/drugs').then(res => setDrugs(res.data));
  }, []);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Drug Name</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Status</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {drugs.map((drug) => (
            <TableRow key={drug.id}>
              <TableCell>{drug.name}</TableCell>
              <TableCell>{drug.quantity}</TableCell>
              <TableCell style={{ color: drug.quantity <= drug.threshold ? 'red' : 'green' }}>
                {drug.quantity <= drug.threshold ? 'Critically Low' : 'Adequate'}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}