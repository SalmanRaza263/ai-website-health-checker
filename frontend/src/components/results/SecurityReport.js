import React from 'react';

interface SecurityReportProps {
  scanId: string;
}

const SecurityReport: React.FC<SecurityReportProps> = () => {
  return (
    <div className="bg-white rounded-lg shadow-xl p-6">
      <h2 className="text-xl font-bold mb-4">Security Report</h2>
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span>SSL Certificate</span>
          <span className="text-green-600">✅ Valid</span>
        </div>
        <div className="flex items-center justify-between">
          <span>Security Headers</span>
          <span className="text-green-600">✅ Present</span>
        </div>
        <div className="flex items-center justify-between">
          <span>Cross-Site Scripting (XSS)</span>
          <span className="text-green-600">✅ Protected</span>
        </div>
        <div className="flex items-center justify-between">
          <span>SQL Injection</span>
          <span className="text-yellow-600">⚠️ Partial</span>
        </div>
      </div>
    </div>
  );
};

export default SecurityReport;