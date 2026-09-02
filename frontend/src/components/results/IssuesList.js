import React from 'react';

interface IssuesListProps {
  scanId: string;
}

const IssuesList: React.FC<IssuesListProps> = () => {
  const issues = [
    { id: 1, category: 'Performance', message: 'Large images detected', severity: 'high' },
    { id: 2, category: 'Accessibility', message: 'Missing alt tags', severity: 'medium' },
    { id: 3, category: 'SEO', message: 'Missing meta description', severity: 'low' }
  ];

  return (
    <div className="bg-white rounded-lg shadow-xl p-6">
      <h2 className="text-xl font-bold mb-4">Issues Found</h2>
      <div className="space-y-3">
        {issues.map((issue) => (
          <div key={issue.id} className="border-b pb-2">
            <div className="flex items-center justify-between">
              <span className="font-medium">{issue.category}</span>
              <span className={`text-sm px-2 py-1 rounded ${
                issue.severity === 'high' ? 'bg-red-100 text-red-600' :
                issue.severity === 'medium' ? 'bg-yellow-100 text-yellow-600' :
                'bg-blue-100 text-blue-600'
              }`}>
                {issue.severity}
              </span>
            </div>
            <p className="text-sm text-gray-600">{issue.message}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default IssuesList;