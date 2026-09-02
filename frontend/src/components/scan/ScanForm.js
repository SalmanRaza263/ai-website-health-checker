import React, { useState } from 'react';

const ScanForm = ({ onScanComplete }) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      const mockData = {
        id: `scan_${Date.now()}`,
        url: url,
        status: 'completed'
      };
      onScanComplete(mockData);
      setUrl('');
    } catch (err) {
      setError('Failed to start scan. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-xl p-6">
      <h2 className="text-xl font-bold mb-4">Start New Scan</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Website URL
          </label>
          <input
            type="url"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-400"
        >
          {loading ? 'Scanning...' : 'Start Scan'}
        </button>
        {error && <div className="text-red-600 text-sm">{error}</div>}
      </form>
    </div>
  );
};

export default ScanForm;