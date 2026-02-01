import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { BarChart3, AlertCircle, CheckCircle, TrendingUp, Package, Calendar, Wrench } from 'lucide-react'
import { instrumentsService, consumablesService, calibrationsService, inventoryTransactionsService } from '../../../services/labManagementApi'
import toast from 'react-hot-toast'
import Card from '../../../components/labManagement/Card'
import Badge from '../../../components/labManagement/Badge'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts'

function InventoryReports() {
  const [summary, setSummary] = useState(null)
  const [calibrationCompliance, setCalibrationCompliance] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadReports()
  }, [])

  const loadReports = async () => {
    try {
      setLoading(true)

      // Fetch all data in parallel
      const [instruments, calibrations, consumables] = await Promise.all([
        instrumentsService.getAll(),
        calibrationsService.getAll(),
        consumablesService.getAll()
      ])

      // Calculate summary statistics
      const activeInstruments = instruments.filter(i => i.status === 'Active').length
      const instrumentsUnderMaintenance = instruments.filter(i => i.status === 'Under Maintenance').length
      const lowStockItems = consumables.filter(c => c.status === 'Low Stock' || c.status === 'Out of Stock').length
      const expiringItems = consumables.filter(c => c.status === 'Expiring Soon' || c.status === 'Expired').length
      const upcomingCalibrations = calibrations.filter(c => c.status === 'Due Soon').length
      const overdueCalibrations = calibrations.filter(c => c.status === 'Overdue').length
      const instrumentUtilization = instruments.length > 0 ? (activeInstruments / instruments.length) * 100 : 0

      setSummary({
        totalInstruments: instruments.length,
        activeInstruments,
        instrumentsUnderMaintenance,
        totalConsumables: consumables.length,
        lowStockItems,
        expiringItems,
        upcomingCalibrations,
        overdueCalibrations,
        instrumentUtilization
      })

      // Calculate calibration compliance
      const calibrated = calibrations.filter(c => c.status === 'Valid').length
      const dueSoon = calibrations.filter(c => c.status === 'Due Soon').length
      const overdue = calibrations.filter(c => c.status === 'Overdue').length
      const complianceRate = calibrations.length > 0 ? (calibrated / calibrations.length) * 100 : 0

      setCalibrationCompliance({
        calibrated,
        dueSoon,
        overdue,
        complianceRate
      })
    } catch (error) {
      console.error('Error loading reports:', error)
      toast.error('Failed to load reports')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
          <p className="mt-4 text-gray-600">Loading reports...</p>
        </div>
      </div>
    )
  }

  const statusData = summary ? [
    { name: 'Active', value: summary.activeInstruments, color: '#10b981' },
    { name: 'Maintenance', value: summary.instrumentsUnderMaintenance, color: '#f59e0b' },
    { name: 'Out of Service', value: summary.totalInstruments - summary.activeInstruments - summary.instrumentsUnderMaintenance, color: '#ef4444' }
  ] : []

  const calibrationComplianceData = calibrationCompliance ? [
    { name: 'Calibrated', value: calibrationCompliance.calibrated, color: '#10b981' },
    { name: 'Due Soon', value: calibrationCompliance.dueSoon, color: '#f59e0b' },
    { name: 'Overdue', value: calibrationCompliance.overdue, color: '#ef4444' }
  ] : []

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
      >
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-600 flex items-center justify-center shadow-lg">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            Inventory Reports & Dashboard
          </h1>
          <p className="text-gray-600 mt-1">View inventory summaries, compliance reports, and analytics</p>
        </div>
      </motion.div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Instruments</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{summary?.totalInstruments || 0}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center">
              <Wrench className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-sm text-gray-500">Total: {summary?.totalInstruments || 0}</span>
            <span className="text-sm text-green-600 font-medium">Active: {summary?.activeInstruments || 0}</span>
          </div>
        </Card>
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Consumables</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{summary?.totalConsumables || 0}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
              <Package className="w-6 h-6 text-purple-600" />
            </div>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-sm text-gray-500">Total: {summary?.totalConsumables || 0}</span>
            <span className="text-sm text-red-600 font-medium">Low Stock: {summary?.lowStockItems || 0}</span>
          </div>
        </Card>
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Low Stock Items</p>
              <p className="text-2xl font-bold text-orange-600 mt-1">{summary?.lowStockItems || 0}</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-orange-100 flex items-center justify-center">
              <AlertCircle className="w-6 h-6 text-orange-600" />
            </div>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-sm text-gray-500">Compliance: {calibrationCompliance?.complianceRate?.toFixed(1) || 0}%</span>
            <span className="text-sm text-purple-600 font-medium">Utilization: {summary?.instrumentUtilization?.toFixed(1) || 0}%</span>
          </div>
        </Card>
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Calibration Compliance</p>
              <p className="text-2xl font-bold text-green-600 mt-1">{calibrationCompliance?.complianceRate?.toFixed(1) || 0}%</p>
            </div>
            <div className="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Instrument Status Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={statusData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {statusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Card>

        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Calibration Compliance</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={calibrationComplianceData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {calibrationComplianceData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </Card>
      </div>

      {/* Alerts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-orange-600" />
            Upcoming Calibrations
          </h3>
          <div className="space-y-2">
            {summary?.upcomingCalibrations > 0 ? (
              <div className="p-3 bg-orange-50 rounded-lg border border-orange-200">
                <p className="text-sm font-medium text-orange-900">
                  {summary.upcomingCalibrations} calibration(s) due within 30 days
                </p>
              </div>
            ) : (
              <p className="text-sm text-gray-500">No upcoming calibrations</p>
            )}
            {summary?.overdueCalibrations > 0 && (
              <div className="p-3 bg-red-50 rounded-lg border border-red-200">
                <p className="text-sm font-medium text-red-900">
                  {summary.overdueCalibrations} overdue calibration(s) require immediate attention
                </p>
              </div>
            )}
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Package className="w-5 h-5 text-purple-600" />
            Stock Alerts
          </h3>
          <div className="space-y-2">
            {summary?.lowStockItems > 0 ? (
              <div className="p-3 bg-orange-50 rounded-lg border border-orange-200">
                <p className="text-sm font-medium text-orange-900">
                  {summary.lowStockItems} item(s) are below threshold
                </p>
              </div>
            ) : (
              <p className="text-sm text-gray-500">All items are well stocked</p>
            )}
            {summary?.expiringItems > 0 && (
              <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                <p className="text-sm font-medium text-yellow-900">
                  {summary.expiringItems} item(s) expiring within 30 days
                </p>
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  )
}

export default InventoryReports
