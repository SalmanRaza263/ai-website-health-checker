import React from 'react';
import { motion } from 'framer-motion';

const CategoryScore = ({ scanId, categories = [] }) => {
  const defaultCategories = [
    { name: 'Performance', score: 85, description: 'Page load speed' },
    { name: 'Accessibility', score: 92, description: 'Screen reader support' },
    { name: 'Best Practices', score: 78, description: 'Code quality' },
    { name: 'SEO', score: 88, description: 'Search engine optimization' }
  ];

  const data = categories.length > 0 ? categories : defaultCategories;

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBackground = (score) => {
    if (score >= 90) return 'bg-green-500';
    if (score >= 70) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getScoreLabel = (score) => {
    if (score >= 90) return 'Excellent';
    if (score >= 70) return 'Good';
    if (score >= 50) return 'Needs Improvement';
    return 'Poor';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-white rounded-lg shadow-xl p-6 max-w-2xl mx-auto"
    >
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Category Scores</h2>
        <span className="text-sm text-gray-500">ID: {scanId}</span>
      </div>

      <div className="space-y-5">
        {data.map((category, index) => (
          <motion.div
            key={category.name}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-gray-50 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between mb-2">
              <div>
                <h3 className="font-semibold text-gray-800">{category.name}</h3>
                {category.description && (
                  <p className="text-sm text-gray-500">{category.description}</p>
                )}
              </div>
              <span className={`font-bold text-lg ${getScoreColor(category.score)}`}>
                {category.score}%
              </span>
            </div>

            <div className="relative">
              <div className="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                <motion.div
                  className={`h-full ${getScoreBackground(category.score)} rounded-full`}
                  initial={{ width: 0 }}
                  animate={{ width: `${category.score}%` }}
                  transition={{ duration: 0.8, delay: 0.2 + index * 0.1 }}
                />
              </div>
              <span className="absolute -top-6 right-0 text-xs font-medium text-gray-600">
                {getScoreLabel(category.score)}
              </span>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex justify-between text-sm text-gray-600">
          <span>🔴 Needs attention</span>
          <span>🟡 Good</span>
          <span>🟢 Excellent</span>
        </div>
      </div>
    </motion.div>
  );
};

export default CategoryScore;