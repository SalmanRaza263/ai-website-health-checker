import React from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { URLInput } from '../components/home/URLInput'
import { Features } from '../components/home/Features'
import { useScan } from '../hooks/useScan'

export const Home = () => {
  const navigate = useNavigate()
  const { startScan, loading } = useScan()

  const handleScan = async (url: string) => {
    const scanId = await startScan(url)
    if (scanId) {
      navigate(`/scan?scanId=${scanId}`)
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
          AI Website Health Checker
        </h1>
        <p className="text-gray-400 text-lg max-w-2xl mx-auto">
          Analyze your website's security, performance, SEO, and accessibility in real-time
        </p>
      </motion.div>

      {/* URL Input */}
      <URLInput onScan={handleScan} loading={loading} />

      {/* Features */}
      <Features />

      {/* Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-12"
      >
        {[
          { label: 'Security Checks', value: '15+' },
          { label: 'Performance Metrics', value: '10+' },
          { label: 'SEO Factors', value: '20+' },
          { label: 'Accessibility Rules', value: '50+' }
        ].map((stat, index) => (
          <div key={index} className="glass rounded-xl p-6 text-center">
            <p className="text-3xl font-bold text-blue-400">{stat.value}</p>
            <p className="text-gray-400 text-sm">{stat.label}</p>
          </div>
        ))}
      </motion.div>
    </div>
  )
}