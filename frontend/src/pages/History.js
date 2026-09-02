import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { Calendar, Eye, AlertCircle, CheckCircle } from 'lucide-react'
import { useScan } from '../hooks/useScan'
import { Loader } from '../components/common/Loader'

export const History = () => {
  const navigate = useNavigate()
  const { getHistory, history, loading } = useScan()

  useEffect(() => {
    getHistory()
  }, [])

  if (loading) {
    return <Loader />
  }

  return (
    <div className="max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-8">
          Scan History
        </h1>

        {history.length === 0 ? (
          <div className="text-center py-12">
            <AlertCircle className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400 text-lg">No scans found</p>
            <p className="text-gray-500">Start your first scan from the home page</p>
          </div>
        ) : (
          <div className="space-y-4">
            {history.map((scan: any) => (
              <div
                key={scan.id}
                className="glass rounded-xl p-6 hover:border-blue-500/50 transition-all duration-300 cursor-pointer"
                onClick={() => navigate(`/results/${scan.id}`)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    {scan.status === 'completed' ? (
                      <CheckCircle className="w-6 h-6 text-green-400" />
                    ) : scan.status === 'failed' ? (
                      <AlertCircle className="w-6 h-6 text-red-400" />
                    ) : (
                      <div className="w-6 h-6 border-2 border-yellow-400 border-t-transparent rounded-full animate-spin" />
                    )}
                    <div>
                      <p className="font-medium">{scan.url}</p>
                      <div className="flex items-center gap-4 text-sm text-gray-400">
                        <span className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {new Date(scan.created_at).toLocaleString()}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          scan.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                          scan.status === 'failed' ? 'bg-red-500/20 text-red-400' :
                          'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {scan.status}
                        </span>
                      </div>
                    </div>
                  </div>
                  <Eye className="w-5 h-5 text-gray-400 hover:text-white transition-colors" />
                </div>
              </div>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  )
}