import React from 'react'
import { FlaskConical, CheckCircle, Clock, FileText, AlertCircle } from 'lucide-react'
import Button from '../Button'
import Badge from '../Badge'

function SampleTestPlanModal({ isOpen, onClose, testPlan }) {
    if (!isOpen) return null

    // Sample data to augment the existing test plan or provide defaults
    const sampleSteps = [
        { id: 1, name: 'Initial Setup', description: 'Configure test equipment according to ISO 17025', status: 'Completed' },
        { id: 2, name: 'Calibration Check', description: 'Verify calibration status of all sensors', status: 'Completed' },
        { id: 3, name: 'Run Test Cycle 1', description: 'Execute primary test sequence at 25°C', status: 'In Progress' },
        { id: 4, name: 'Data Recording', description: 'Log all parameters every 5 seconds', status: 'Pending' },
        { id: 5, name: 'Final Analysis', description: 'Analyze results against acceptance criteria', status: 'Pending' },
    ]

    const statusColors = {
        Completed: 'success',
        'In Progress': 'warning',
        Pending: 'default'
    }

    return (
        <div className="space-y-6">
            <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
                <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-lg bg-white border border-gray-200 flex items-center justify-center shadow-sm">
                        <FlaskConical className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                        <h3 className="text-lg font-bold text-gray-900">{testPlan?.name || 'Sample Test Plan'}</h3>
                        <p className="text-gray-600 text-sm mt-1">{testPlan?.description || 'Comprehensive test plan for validation.'}</p>
                        <div className="flex gap-2 mt-2">
                            <Badge variant="info">{testPlan?.testType || 'EMC'}</Badge>
                            <Badge variant="default">Rev 1.0</Badge>
                            <Badge variant="success">Active</Badge>
                        </div>
                    </div>
                </div>
            </div>

            <div>
                <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                    <FileText className="w-4 h-4 text-gray-500" />
                    Test Steps
                </h4>
                <div className="space-y-3">
                    {sampleSteps.map((step) => (
                        <div key={step.id} className="flex items-center gap-3 p-3 bg-white border border-gray-200 rounded-lg hover:shadow-sm transition-shadow">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${step.status === 'Completed' ? 'bg-green-100 text-green-600' :
                                    step.status === 'In Progress' ? 'bg-yellow-100 text-yellow-600' :
                                        'bg-gray-100 text-gray-400'
                                }`}>
                                {step.status === 'Completed' ? <CheckCircle className="w-4 h-4" /> :
                                    step.status === 'In Progress' ? <Clock className="w-4 h-4" /> :
                                        <span className="text-xs font-bold">{step.id}</span>}
                            </div>
                            <div className="flex-1">
                                <div className="flex justify-between">
                                    <span className="font-medium text-gray-900">{step.name}</span>
                                    <Badge variant={statusColors[step.status]}>{step.status}</Badge>
                                </div>
                                <p className="text-sm text-gray-500">{step.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                <h4 className="font-bold text-blue-900 mb-2 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4" />
                    Acceptance Criteria
                </h4>
                <ul className="list-disc list-inside text-sm text-blue-800 space-y-1">
                    <li>Signal to Noise ratio must be &gt; 20dB</li>
                    <li>Temperature rise must not exceed 40°C</li>
                    <li>No visible damage or deformation after test</li>
                </ul>
            </div>

            <div className="flex justify-end pt-4 border-t border-gray-100">
                <Button onClick={onClose}>Close</Button>
            </div>
        </div>
    )
}

export default SampleTestPlanModal
