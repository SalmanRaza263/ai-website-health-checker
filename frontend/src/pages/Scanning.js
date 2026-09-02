import React, { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ScanProgress } from '../components/scan/ScanProgress'
import { LiveLogs } from '../components/scan/LiveLogs'
import { LoadingAnimation } from '../components/scan/ScanningAnimation'
import { useScan } from '../hooks/useScan'

export const Scanning = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [scanId, setScanId] = useState<string | null>(null)
  const { getScanStatus, scanStatus } = useScan()

  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const id = params.get('scanId')
    if (id) {
      setScanId(id)
      pollScanStatus(id)
    } else {
      navigate('/')
    }
  }, [location])

  const pollScanStatus = async (id: string) => {
    const interval = setInterval(async () => {
      const status = await getScanStatus(id)
      if (status?.status === 'completed' || status?.status === 'failed') {
        clearInterval(interval)
        if (status?.status === 'completed') {
          navigate(`/results/${id}`)
        }
      }
    }, 2000)

    return () => clearInterval(interval)
  }

  if (!scanId) {
    return null
  }

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          Scanning Website
        </h1>
        <p className="text-gray-400 mt-2">Please wait while we analyze the website</p>
      </motion.div>

      <div className="space-y-8">
        <ScanProgress scanId={scanId} />
        <LiveLogs scanId={scanId} />
        <LoadingAnimation />
      </div>
    </div>
  )
}