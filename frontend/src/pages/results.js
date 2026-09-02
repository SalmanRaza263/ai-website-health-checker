import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Dashboard } from '../components/results/Dashboard'
import { CategoryScore } from '../components/results/CategoryScore'
import { SecurityReport } from '../components/results/SecurityReport'
import { PerformanceMetrics } from '../components/results/PerformanceMetrics'
import { TechnologyStack } from '../components/results/TechnologyStack'
import { DownloadReport } from '../components/results/DownloadReport'
import { useScan } from '../hooks/useScan'
import { Loader } from '../components/common/Loader'

export const Results = () => {
  const { scanId } = useParams()
  const navigate = useNavigate()
  const { getScanStatus, scanStatus } = useScan()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!scanId) {
      navigate('/')
      return
    }

    const fetchResults = async () => {
      const status = await getScanStatus(scanId)
      if (status?.status === 'completed') {
        setLoading(false)
      } else if (status?.status === 'failed') {
        navigate('/')
      }
    }

    fetchResults()
  }, [scanId])

  if (loading) {
    return <Loader />
  }

  return (
    <div className="max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-8"
      >
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Scan Results
          </h1>
          <DownloadReport scanId={scanId!} />
        </div>

        <Dashboard scanId={scanId!} />
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <CategoryScore scanId={scanId!} />
          <SecurityReport scanId={scanId!} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <PerformanceMetrics scanId={scanId!} />
          <TechnologyStack scanId={scanId!} />
        </div>
      </motion.div>
    </div>
  )
}