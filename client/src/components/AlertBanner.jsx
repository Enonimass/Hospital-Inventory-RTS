import { Alert } from '@mui/material';
import api from '../services/api';

export default function AlertBanner() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    api.get('/alerts').then(res => setAlerts(res.data));
  }, []);

  return (
    <>
      {alerts.map((alert) => (
        <Alert severity="error" key={alert.id}>{alert.message}</Alert>
      ))}
    </>
  );
}