import React from 'react'
import { FileText, Download, Share2, CheckCircle, BarChart3, Calendar, User } from 'lucide-react'
import Button from '../Button'
import Badge from '../Badge'

function SampleTestResultModal({ isOpen, onClose, result }) {
    if (!isOpen) return null

    const isPass = result?.passFail !== false // Default to pass if undefined

    return (
        <div className="space-y-6">
            {/* Header Section */}
            <div className="flex flex-col sm:flex-row justify-between items-start gap-4 pb-4 border-b border-gray-100">
                <div className="flex items-start gap-4">
                    <div className={`w-16 h-16 rounded-xl flex items-center justify-center shadow-sm ${isPass ? 'bg-green-100' : 'bg-red-100'}`}>
                        <BarChart3 className={`w-8 h-8 ${isPass ? 'text-green-600' : 'text-red-600'}`} />
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-gray-900">Test Report: {result?.id || 'TR-2026-889'}</h2>
                        <div className="flex items-center gap-2 mt-1">
                            <span className={`text-sm font-bold ${isPass ? 'text-green-600' : 'text-red-600'}`}>
                                {isPass ? 'PASS' : 'FAIL'}
                            </span>
                            <span className="text-gray-300">•</span>
                            <span className="text-sm text-gray-500">{result?.testType || 'EMC Testing'}</span>
                        </div>
                    </div>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm" icon={<Share2 className="w-4 h-4" />}>Share</Button>
                    <Button
                        variant="default"
                        size="sm"
                        icon={<Download className="w-4 h-4" />}
                        onClick={() => {
                            if (result?.attachments && result.attachments.length > 0) {
                                const url = result.attachments[0]
                                window.open(url, '_blank')
                            } else {
                                alert('No report file attached')
                            }
                        }}
                    >
                        Download Report
                    </Button>
                </div>
            </div>

            {/* Summary Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="text-xs text-gray-500 uppercase font-bold mb-1">Date</div>
                    <div className="flex items-center gap-2 text-sm font-medium text-gray-900">
                        <Calendar className="w-4 h-4 text-gray-400" />
                        {new Date().toLocaleDateString()}
                    </div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="text-xs text-gray-500 uppercase font-bold mb-1">Engineer</div>
                    <div className="flex items-center gap-2 text-sm font-medium text-gray-900">
                        <User className="w-4 h-4 text-gray-400" />
                        John Doe
                    </div>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="text-xs text-gray-500 uppercase font-bold mb-1">Reference</div>
                    <div className="flex items-center gap-2 text-sm font-medium text-gray-900">
                        <FileText className="w-4 h-4 text-gray-400" />
                        ISO 17025-2017
                    </div>
                </div>
            </div>

            {/* Charts / Data Mockup */}
            <div className="border border-gray-200 rounded-xl p-4">
                <h4 className="font-bold text-gray-900 mb-4">Measurement Data</h4>
                <div className="space-y-4">
                    {/* Mock Chart Bar 1 */}
                    <div className="space-y-1">
                        <div className="flex justify-between text-xs font-medium">
                            <span>Signal Strength (dBm)</span>
                            <span className="text-green-600">-45 dBm (Pass)</span>
                        </div>
                        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                            <div className="h-full bg-green-500 w-[75%]"></div>
                        </div>
                    </div>
                    {/* Mock Chart Bar 2 */}
                    <div className="space-y-1">
                        <div className="flex justify-between text-xs font-medium">
                            <span>Frequency Stability (Hz)</span>
                            <span className="text-green-600">0.05 Hz (Pass)</span>
                        </div>
                        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                            <div className="h-full bg-blue-500 w-[90%]"></div>
                        </div>
                    </div>
                    {/* Mock Chart Bar 3 */}
                    <div className="space-y-1">
                        <div className="flex justify-between text-xs font-medium">
                            <span>Power Consumption (W)</span>
                            <span className="text-yellow-600">145 W (Warning)</span>
                        </div>
                        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                            <div className="h-full bg-yellow-500 w-[60%]"></div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Observations */}
            <div>
                <h4 className="font-bold text-gray-900 mb-2">Observations & Conclusion</h4>
                <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-700 leading-relaxed">
                    <p className="mb-2">
                        The device under test (DUT) performed within valid parameters for the majority of the test cycle.
                        Signal integrity remained strong despite interference.
                    </p>
                    <p className="font-medium text-gray-900">
                        Conclusion: The DUT meets the requirements for certification.
                    </p>
                </div>
            </div>

            <div className="flex justify-end pt-4 border-t border-gray-100">
                <Button onClick={onClose}>Close Report</Button>
            </div>
        </div>
    )
}

export default SampleTestResultModal
