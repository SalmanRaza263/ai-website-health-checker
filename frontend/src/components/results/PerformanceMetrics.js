import React from 'react';

interface PerformanceMetricsProps {
  scanId: string;
}

const PerformanceMetrics: React.FC<PerformanceMetricsProps> = () => {
  return (
    <div className="bg-white rounded-lg shadow-xl p-6">
      <h2 className="text-xl font-bold mb-4">Performance Metrics</h2>
      <div className="space-y-4">
        <div>
          <div className="flex justify-between text-sm">
            <span>Page Load Time</span>
            <span>2.3s</span>
          </div>
          <div className="w-full h-2 bg-gray-200 rounded-full mt-1">
            <div className="h-2 bg-green-500 rounded-full" style={{ width: '85%' }}></div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-sm">
            <span>First Paint</span>
            <span>1.2s</span>
          </div>
          <div className="w-full h-2 bg-gray-200 rounded-full mt-1">
            <div className="h-2 bg-blue-500 rounded-full" style={{ width: '70%' }}></div>
          </div>
        </div>
        <div>
          <div className="flex justify-between text-sm">
            <span>Time to Interactive</span>
            <span>3.1s</span>
          </div>
          <div className="w-full h-2 bg-gray-200 rounded-full mt-1">
            <div className="h-2 bg-yellow-500 rounded-full" style={{ width: '60%' }}></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PerformanceMetrics;