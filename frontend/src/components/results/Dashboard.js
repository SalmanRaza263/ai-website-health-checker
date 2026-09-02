import React from 'react';
import { motion } from 'framer-motion';
import { BarChart3, AlertTriangle, CheckCircle, Clock } from 'lucide-react';
import CategoryScore from './CategoryScore';
import IssuesList from './IssuesList';
import PerformanceMetrics from './PerformanceMetrics';
import SecurityReport from './SecurityReport';

const Dashboard = ({ scanId }) => {
  if (!scanId) {
    return (
      <div className="bg-white rounded-lg shadow-xl p-8 text-center">
        <AlertTriangle className="h-12 w-12 text-gray-400 mx-auto mb-3" />
        <p className="text-gray-500">No scan results yet. Start a new scan!</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="space-y-6 mt-6"
    >
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center">
            <CheckCircle className="h-5 w-5 text-green-500" />
            <span className="ml-2 text-sm text-gray-600">Passed</span>
          </div>
          <p className="text-2xl font-bold mt-1">12</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center">
            <AlertTriangle className="h-5 w-5 text-yellow-500" />
            <span className="ml-2 text-sm text-gray-600">Warnings</span>
          </div>
          <p className="text-2xl font-bold mt-1">3</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center">
            <BarChart3 className="h-5 w-5 text-blue-500" />
            <span className="ml-2 text-sm text-gray-600">Score</span>
          </div>
          <p className="text-2xl font-bold mt-1">85%</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center">
            <Clock className="h-5 w-5 text-purple-500" />
            <span className="ml-2 text-sm text-gray-600">Time</span>
          </div>
          <p className="text-2xl font-bold mt-1">2.3s</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CategoryScore scanId={scanId} />
        <PerformanceMetrics scanId={scanId} />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <IssuesList scanId={scanId} />
        <SecurityReport scanId={scanId} />
      </div>
    </motion.div>
  );
};

export default Dashboard;