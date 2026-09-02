export interface ScanResults {
  url: string
  status: string
  results: {
    health?: {
      status_code: number
      response_time: number
      server?: string
      content_type?: string
      content_length?: number
    }
    security_headers?: {
      'Content-Security-Policy'?: string
      'Strict-Transport-Security'?: string
      'X-Frame-Options'?: string
      'X-Content-Type-Options'?: string
      'Referrer-Policy'?: string
      'Permissions-Policy'?: string
      score?: string
    }
    ssl?: {
      valid: boolean
      issuer?: string
      subject?: string
      valid_from?: string
      valid_to?: string
      days_left?: number
      protocol?: string
      cipher_suite?: string
    }
    ports?: Array<{
      port: number
      protocol: string
      service: string
      state: string
    }>
    technologies?: {
      technologies: Array<{
        name: string
        category: string
        version?: string
      }>
      count: number
    }
    seo?: {
      title: string
      title_length: number
      description: string
      description_length: number
      keywords: string
      h1: number
      h2: number
      h3: number
      h4: number
      images: number
      alt_text: number
      links: number
      internal_links: number
      external_links: number
      canonical: string
      robots: string
      sitemap: string
      seo_score: number
    }
    performance?: {
      load_time: string
      page_size: string
      requests: number
      scripts: number
      styles: number
      images: number
      status_code: number
    }
    accessibility?: {
      aria_labels: number
      alt_text_images: number
      total_images: number
      semantic_elements: number
      header_structure: boolean
      landmarks: string[]
      issues: string[]
      score: number
    }
    broken_links?: {
      total_links: number
      checked: number
      broken_links: string[]
      working_links: string[]
      broken_count: number
    }
    overall_score?: number
    timestamp?: string
  }
  message: string
}

export interface ScanHistory {
  id: string
  url: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  created_at: string
  completed_at?: string
  overall_score?: number
}

export interface Issue {
  id: string
  scan_id: string
  category: string
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info'
  title: string
  description: string
  recommendation: string
  cve_id?: string
  location?: string
  created_at: string
}

export interface Technology {
  name: string
  category: string
  version?: string
  confidence?: number
}