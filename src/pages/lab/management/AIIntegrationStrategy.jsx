import { motion } from 'framer-motion'
import Card from '../../../components/labManagement/Card'

function AIIntegrationStrategy() {
  const initiatives = [
    {
      title: 'Intelligent Document Processing',
      priority: 'High priority',
      areas: ['Organization Details', 'Manpower', 'Scope Management'],
      summary:
        'Use OCR + LLMs to extract key data from certificates, resumes, calibration reports and auto-fill registration forms.',
      benefits: [
        '90% reduction in manual data entry',
        '10x faster form completion',
        'Automatic validation of uploaded documents',
      ],
    },
    {
      title: 'AI-Powered Validation Assistant',
      priority: 'High priority',
      areas: ['Checklist (Step 12)', 'Registration workflow'],
      summary:
        'Continuously review all registration data, flag missing / inconsistent fields and predict approval readiness.',
      benefits: [
        'Real-time validation feedback',
        'Lower rejection / rework rates',
        'Compliance guidance for users',
      ],
    },
    {
      title: 'Conversational AI Assistant',
      priority: 'Medium priority',
      areas: ['All registration & lab-management screens'],
      summary:
        'Context-aware chatbot that can answer compliance questions, guide users through steps and help with form filling.',
      benefits: [
        '24/7 contextual support',
        'Reduced training effort for new users',
        'Fewer support tickets for routine queries',
      ],
    },
    {
      title: 'Predictive Equipment Maintenance',
      priority: 'High value',
      areas: ['Scope Management → Equipment', 'Quality & audits'],
      summary:
        'Predict calibration / maintenance due dates and potential failures based on usage history and past issues.',
      benefits: [
        'Fewer unplanned equipment outages',
        'Better utilization of lab slots',
        'Improved audit readiness',
      ],
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Integration Strategy</h1>
          <p className="mt-2 text-gray-600 max-w-2xl">
            High-impact AI initiatives to turn the Lab Management System into an intelligent, assistive platform.
            This page is a practical, product-facing view of the full strategy documented in{' '}
            <code>AI_INTEGRATION_STRATEGY.md</code>.
          </p>
        </div>
        <div className="rounded-xl bg-blue-50 border border-blue-200 px-4 py-3 text-sm text-blue-800 max-w-sm">
          <p className="font-semibold">Source of truth</p>
          <p className="mt-1">
            The complete technical and product details live in the root document{' '}
            <code>AI_INTEGRATION_STRATEGY.md</code> in this repository.
          </p>
        </div>
      </div>

      {/* Executive summary */}
      <Card className="p-6 bg-gradient-to-r from-sky-50 to-emerald-50 border-sky-100">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Executive Summary</h2>
            <p className="mt-2 text-gray-700 max-w-3xl">
              The goal is to augment every critical step of the lab lifecycle with AI — from document ingestion and
              registration, through scope and manpower management, to ongoing quality and maintenance — while keeping
              humans in control of final decisions.
            </p>
          </div>
          <ul className="text-sm text-gray-700 space-y-1">
            <li>• Automate repetitive data entry</li>
            <li>• Proactively detect issues and gaps</li>
            <li>• Provide guided, conversational assistance</li>
            <li>• Improve utilization, compliance and turnaround time</li>
          </ul>
        </div>
      </Card>

      {/* Initiatives */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {initiatives.map((item, index) => (
          <motion.div
            key={item.title}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
          >
            <Card className="h-full flex flex-col border border-gray-200">
              <div className="p-5 flex-1 flex flex-col">
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{item.title}</h3>
                    <p className="text-xs font-medium text-blue-700 bg-blue-50 inline-flex px-2 py-0.5 rounded-full mt-1">
                      {item.priority}
                    </p>
                  </div>
                  <div className="text-xs text-gray-500 text-right">
                    <p className="font-medium mb-1">Primary areas</p>
                    <ul>
                      {item.areas.map((area) => (
                        <li key={area}>• {area}</li>
                      ))}
                    </ul>
                  </div>
                </div>
                <p className="text-sm text-gray-700 mb-4">{item.summary}</p>
                <div className="mt-auto">
                  <p className="text-xs font-semibold text-gray-600 mb-1">Key benefits</p>
                  <ul className="text-xs text-gray-700 space-y-1">
                    {item.benefits.map((b) => (
                      <li key={b}>• {b}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Next steps */}
      <Card className="p-5 border border-amber-200 bg-amber-50/40">
        <h2 className="text-sm font-semibold text-amber-900 mb-2">Implementation notes</h2>
        <ul className="text-sm text-amber-900 space-y-1">
          <li>
            • Use this page during demos to explain <span className="font-medium">where</span> AI fits into the LMS and{' '}
            <span className="font-medium">which modules</span> will benefit first.
          </li>
          <li>
            • The engineering references, example prompts and API snippets remain in{' '}
            <code>AI_INTEGRATION_STRATEGY.md</code> to keep the UI focused and non-technical.
          </li>
        </ul>
      </Card>
    </div>
  )
}

export default AIIntegrationStrategy

