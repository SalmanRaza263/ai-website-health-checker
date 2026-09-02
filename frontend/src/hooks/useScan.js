import { useState, useEffect } from 'react';

export const useScan = (scanId) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (scanId) {
      setLoading(false);
      setData({ id: scanId, status: 'completed' });
    }
  }, [scanId]);

  return { data, loading, error };
};