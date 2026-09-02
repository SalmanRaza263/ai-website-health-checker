import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Activity, Shield, Globe, TrendingUp, Clock } from 'lucide-react';
import { scanAPI } from './services/api';
import toast, { Toaster } from 'react-hot-toast';
import Dashboard from './components/results/Dashboard';
import ScanForm from './components/scan/ScanForm';
import CategoryScore from './components/results/CategoryScore';

const Home = () => {
  const [scanId, setScanId] = useState('');
  const [recentScans, setRecentScans] = useState([]);

  useEffect(() => {
    fetchRecentScans();
  }, []);

  const fetchRecentScans = async () => {
    try {
      const result = await scanAPI.getRecent();
      if (result.success) {
        setRecentScans(result.data);
      }
    } catch (error) {
      console.error('Error fetching scans:', error);
    }
  };

  const handleScanComplete = (data) => {
    setScanId(data.id);
    toast.success('Scan completed successfully!');
    fetchRecentScans();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Activity className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">
                AI Website Health Checker
              </h1>
            </div>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Online
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <ScanForm onScanComplete={handleScanComplete} />
            
            <div className="mt-6 bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold text-gray-700 mb-3">Recent Scans</h3>
              {recentScans.length === 0 ? (
                <p className="text-sm text-gray-500">No recent scans</p>
              ) : (
                <div className="space-y-2">
                  {recentScans.slice(0, 3).map((scan) => (
                    <div key={scan.id} className="flex items-center justify-between text-sm">
                      <span className="text-gray-600 truncate">{scan.website_url}</span>
                      <span className="text-xs text-gray-400">
                        {new Date(scan.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="lg:col-span-2">
            {scanId ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <CategoryScore scanId={scanId} />
                <Dashboard scanId={scanId} />
              </motion.div>
            ) : (
              <div className="bg-white rounded-lg shadow-xl p-12 text-center">
                <div className="flex flex-col items-center">
                  <Globe className="h-16 w-16 text-gray-300 mb-4" />
                  <h3 className="text-xl font-semibold text-gray-700 mb-2">
                    No Scan Results Yet
                  </h3>
                  <p className="text-gray-500 max-w-md">
                    Enter a website URL to start a health check scan.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Globe className="h-5 w-5 text-blue-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm text-gray-500">Total Scans</p>
                <p className="text-xl font-semibold">{recentScans.length}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="h-5 w-5 text-green-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm text-gray-500">Avg Score</p>
                <p className="text-xl font-semibold">85%</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <Clock className="h-5 w-5 text-yellow-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm text-gray-500">Avg Time</p>
                <p className="text-xl font-semibold">2.3s</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Shield className="h-5 w-5 text-purple-600" />
              </div>
              <div className="ml-3">
                <p className="text-sm text-gray-500">Security Score</p>
                <p className="text-xl font-semibold">92%</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;