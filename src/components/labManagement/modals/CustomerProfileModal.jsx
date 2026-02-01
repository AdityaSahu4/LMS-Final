import React from 'react'
import { User, Mail, Phone, MapPin, Building, Calendar, FileText, ArrowUpRight } from 'lucide-react'
import Button from '../Button'
import Badge from '../Badge'

function CustomerProfileModal({ isOpen, onClose, customer }) {
    if (!isOpen) return null

    // Sample data if not provided in customer object
    const profile = {
        ...customer,
        phone: customer?.phone || '+1 (555) 123-4567',
        address: customer?.address || '123 Tech Park, Innovation Blvd, CA',
        description: customer?.description || 'Leading provider of IoT solutions.',
        joinDate: 'Jan 15, 2024',
        totalProjects: 12,
        activeProjects: 3,
        totalSpent: '$45,000'
    }

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row gap-6 items-start">
                <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center text-white text-3xl font-bold shadow-lg shrink-0">
                    {profile.companyName?.charAt(0) || 'C'}
                </div>
                <div className="flex-1">
                    <h3 className="text-2xl font-bold text-gray-900">{profile.companyName}</h3>
                    <p className="text-gray-600 mt-1">{profile.description}</p>

                    <div className="flex flex-wrap gap-4 mt-4 text-sm text-gray-600">
                        <div className="flex items-center gap-2">
                            <Mail className="w-4 h-4 text-gray-400" />
                            {profile.email}
                        </div>
                        <div className="flex items-center gap-2">
                            <Phone className="w-4 h-4 text-gray-400" />
                            {profile.phone}
                        </div>
                        <div className="flex items-center gap-2">
                            <MapPin className="w-4 h-4 text-gray-400" />
                            {profile.address}
                        </div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm text-center">
                    <div className="text-sm text-gray-500 font-medium mb-1">Total Projects</div>
                    <div className="text-2xl font-bold text-gray-900">{profile.totalProjects}</div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm text-center">
                    <div className="text-sm text-gray-500 font-medium mb-1">Active Projects</div>
                    <div className="text-2xl font-bold text-primary">{profile.activeProjects}</div>
                </div>
                <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm text-center">
                    <div className="text-sm text-gray-500 font-medium mb-1">Total Spent</div>
                    <div className="text-2xl font-bold text-green-600">{profile.totalSpent}</div>
                </div>
            </div>

            <div>
                <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                    <FileText className="w-4 h-4 text-gray-500" />
                    Recent Project History
                </h4>
                <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-gray-50 border-b border-gray-200">
                            <tr>
                                <th className="px-4 py-3 font-medium text-gray-500">Project</th>
                                <th className="px-4 py-3 font-medium text-gray-500">Date</th>
                                <th className="px-4 py-3 font-medium text-gray-500">Status</th>
                                <th className="px-4 py-3 font-medium text-gray-500 text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            <tr className="hover:bg-gray-50">
                                <td className="px-4 py-3 font-medium">EMC Certification - Model X</td>
                                <td className="px-4 py-3 text-gray-500">Feb 01, 2026</td>
                                <td className="px-4 py-3"><Badge variant="warning">In Progress</Badge></td>
                                <td className="px-4 py-3 text-right text-primary cursor-pointer hover:underline">View</td>
                            </tr>
                            <tr className="hover:bg-gray-50">
                                <td className="px-4 py-3 font-medium">Safety Testing - Battery Pack</td>
                                <td className="px-4 py-3 text-gray-500">Jan 10, 2026</td>
                                <td className="px-4 py-3"><Badge variant="success">Completed</Badge></td>
                                <td className="px-4 py-3 text-right text-primary cursor-pointer hover:underline">View</td>
                            </tr>
                            <tr className="hover:bg-gray-50">
                                <td className="px-4 py-3 font-medium">RF Analysis - 5G Module</td>
                                <td className="px-4 py-3 text-gray-500">Dec 15, 2025</td>
                                <td className="px-4 py-3"><Badge variant="success">Completed</Badge></td>
                                <td className="px-4 py-3 text-right text-primary cursor-pointer hover:underline">View</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="flex justify-end pt-4 border-t border-gray-100">
                <Button onClick={onClose}>Close Profile</Button>
            </div>
        </div>
    )
}

export default CustomerProfileModal
