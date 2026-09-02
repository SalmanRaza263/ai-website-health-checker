import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || ''
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || ''

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export interface ScanRecord {
  id: string
  url: string
  user_id: string
  status: string
  results: any
  created_at: string
  updated_at: string
  completed_at: string
  overall_score: number
}

export const saveScan = async (scanData: Partial<ScanRecord>) => {
  const { data, error } = await supabase
    .from('scans')
    .insert([scanData])
    .select()
  
  if (error) throw error
  return data?.[0]
}

export const getScans = async (userId?: string) => {
  let query = supabase.from('scans').select('*').order('created_at', { ascending: false })
  
  if (userId) {
    query = query.eq('user_id', userId)
  }
  
  const { data, error } = await query
  if (error) throw error
  return data
}

export const getScanById = async (scanId: string) => {
  const { data, error } = await supabase
    .from('scans')
    .select('*')
    .eq('id', scanId)
    .single()
  
  if (error) throw error
  return data
}

export const updateScan = async (scanId: string, updates: Partial<ScanRecord>) => {
  const { data, error } = await supabase
    .from('scans')
    .update(updates)
    .eq('id', scanId)
    .select()
  
  if (error) throw error
  return data?.[0]
}