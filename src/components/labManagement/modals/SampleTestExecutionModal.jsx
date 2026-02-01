import React, { useState } from 'react'
import { Play, CheckCircle, Clock, AlertTriangle, FileText, ArrowRight } from 'lucide-react'
import Button from '../Button'
import Badge from '../Badge'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'

function SampleTestExecutionModal({ isOpen, onClose, execution }) {
    const navigate = useNavigate()
    const [passingToResults, setPassingToResults] = useState(false)

    if (!isOpen) return null

    const handlePassToResults = async () => {
        setPassingToResults(true)
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        setPassingToResults(false)
        toast.success('Test execution results passed successfully!')
        navigate(`/lab/management/test-results`)
        onClose()
    }

    // Determine if we can pass to results
    // In a real app, this would check status === 'Completed' or similar
    // For sample/demo purposes, allowing it for "Completed", "Passed", "Meet Compliance"
    const canPassToResults = ['completed', 'passed', 'meet compliance'].includes(execution?.status?.toLowerCase())

    return (
        <div className="space-y-6">
            <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-lg bg-white border border-gray-200 flex items-center justify-center shadow-sm">
                        <Play className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                        <h3 className="text-lg font-bold text-gray-900">Execution #{execution?.id || '296'}</h3>
                        <p className="text-gray-600 text-sm mt-1">Executed on {new Date().toLocaleDateString()}</p>
                        <div className="flex gap-2 mt-2">
                            <Badge variant={execution?.status?.toLowerCase() === 'completed' ? 'success' : 'default'}>
                                {execution?.status || 'In Progress'}
                            </Badge>
                            <span className="text-sm text-gray-500 flex items-center gap-1">
                                <Clock className="w-4 h-4" /> 2h 15m duration
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 border border-gray-200 rounded-lg">
                    <h4 className="font-bold text-sm text-gray-700 mb-2">Test Parameters</h4>
                    <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                            <span className="text-gray-500">Temperature:</span>
                            <span className="font-medium">25.4°C</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-500">Humidity:</span>
                            <span className="font-medium">45%</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-gray-500">Voltage:</span>
                            <span className="font-medium">230V</span>
                        </div>
                    </div>
                </div>
                <div className="p-4 border border-gray-200 rounded-lg">
                    <h4 className="font-bold text-sm text-gray-700 mb-2">Equipment Used</h4>
                    <ul className="list-disc list-inside text-sm text-gray-600">
                        <li>Oscilloscope (EQ-2023-001)</li>
                        <li>Function Generator (EQ-2022-045)</li>
                        <li>Multimeter (EQ-2024-012)</li>
                    </ul>
                </div>
            </div>

            <div>
                <h4 className="font-bold text-gray-900 mb-2">Execution Logs</h4>
                <div className="bg-gray-900 text-gray-100 p-4 rounded-lg font-mono text-sm h-48 overflow-y-auto">
                    <div className="flex gap-2 text-gray-400">
                        <span>[10:00:01]</span>
                        <span>Initializing test sequence...</span>
                    </div>
                    <div className="flex gap-2 text-green-400">
                        <span>[10:00:05]</span>
                        <span>Initialization successful.</span>
                    </div>
                    <div className="flex gap-2">
                        <span>[10:00:15]</span>
                        <span>Starting Phase 1: Signal Injection</span>
                    </div>
                    <div className="flex gap-2">
                        <span>[10:05:00]</span>
                        <span>Phase 1 Completed. Readings: 98% nominal</span>
                    </div>
                    <div className="flex gap-2">
                        <span>[10:05:05]</span>
                        <span>Starting Phase 2: Stress Test</span>
                    </div>
                    <div className="flex gap-2 text-yellow-500">
                        <span>[10:15:30]</span>
                        <span>Warning: Temperature spike detected (41°C)</span>
                    </div>
                    <div className="flex gap-2">
                        <span>[10:15:35]</span>
                        <span>Fan speed increased automatically.</span>
                    </div>
                    <div className="flex gap-2 text-green-400">
                        <span>[10:30:00]</span>
                        <span>Test Execution Completed Successfully.</span>
                    </div>
                </div>
            </div>

            <div className="flex justify-between items-center pt-4 border-t border-gray-100">
                <Button variant="outline" onClick={onClose}>Close</Button>
                {canPassToResults && (
                    <Button
                        onClick={handlePassToResults}
                        disabled={passingToResults}
                        className="bg-green-600 hover:bg-green-700 text-white"
                    >
                        {passingToResults ? 'Processing...' : (
                            <span className="flex items-center gap-2">
                                Pass to Test Results <ArrowRight className="w-4 h-4" />
                            </span>
                        )}
                    </Button>
                )}
            </div>
        </div>
    )
}

export default SampleTestExecutionModal
