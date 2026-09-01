export const sidebarLinks = [
  { label: 'Dashboard', icon: 'LayoutGrid' },
  { label: 'Workforce', icon: 'Users' },
  { label: 'Recruitment', icon: 'UserPlus' },
  { label: 'Logistics', icon: 'Truck' },
  { label: 'Warehouse', icon: 'Package' },
  { label: 'Billing', icon: 'CreditCard' },
  { label: 'Payroll', icon: 'Wallet' },
  { label: 'Analytics', icon: 'BarChart3' },
  { label: 'Reports', icon: 'FileText' },
  { label: 'Settings', icon: 'Settings' },
];

export const kpiMetrics = [
  { title: 'Total Employees', value: '1,250', percent: '+3.2%', trend: 'up', icon: 'Users2', color: 'bg-sky-500/10 text-sky-600' },
  { title: 'Employees Present', value: '987', percent: '+1.8%', trend: 'up', icon: 'CheckCircle2', color: 'bg-emerald-500/10 text-emerald-600' },
  { title: 'Active Trucks', value: '42', percent: '-2.5%', trend: 'down', icon: 'Truck', color: 'bg-orange-500/10 text-orange-600' },
  { title: 'Active Deliveries', value: '138', percent: '+7.9%', trend: 'up', icon: 'PackageOpen', color: 'bg-indigo-500/10 text-indigo-600' },
  { title: 'Pending Orders', value: '62', percent: '-4.3%', trend: 'down', icon: 'Clock3', color: 'bg-amber-500/10 text-amber-600' },
  { title: 'Warehouse Stock', value: '24,860 tons', percent: '+6.6%', trend: 'up', icon: 'Archive', color: 'bg-violet-500/10 text-violet-600' },
  { title: 'Monthly Revenue', value: '$1.8M', percent: '+9.4%', trend: 'up', icon: 'DollarSign', color: 'bg-teal-500/10 text-teal-600' },
  { title: 'Monthly Expenses', value: '$1.1M', percent: '-1.2%', trend: 'down', icon: 'TrendingDown', color: 'bg-rose-500/10 text-rose-600' },
];

export const navigationCards = [
  { label: 'Add Employee', icon: 'UserPlus', color: 'from-sky-500 to-cyan-500' },
  { label: 'Create Order', icon: 'FilePlus', color: 'from-indigo-500 to-violet-500' },
  { label: 'Assign Truck', icon: 'Truck', color: 'from-emerald-500 to-lime-500' },
  { label: 'Add Inventory', icon: 'PackagePlus', color: 'from-orange-500 to-amber-500' },
  { label: 'Generate Invoice', icon: 'CreditCard', color: 'from-fuchsia-500 to-pink-500' },
  { label: 'Process Payroll', icon: 'Wallet', color: 'from-rose-500 to-red-500' },
];

export const activityFeed = [
  { time: '08:10 AM', title: 'Employee attendance logged', description: '54 field engineers marked present at Haldia plant.', icon: 'CheckCircle2', tag: 'Attendance' },
  { time: '09:45 AM', title: 'Truck dispatched to port', description: '22-ton shipment departed from warehouse B.', icon: 'Truck', tag: 'Logistics' },
  { time: '10:20 AM', title: 'Invoice generated', description: 'Billing created for order #A-4523.', icon: 'FileText', tag: 'Finance' },
  { time: '11:30 AM', title: 'Candidate shortlist prepared', description: 'Quality engineers shortlisted for site recruitment.', icon: 'UserCheck', tag: 'Recruitment' },
  { time: '12:05 PM', title: 'Stock replenishment scheduled', description: 'Steel coil inventory threshold crossed at warehouse 2.', icon: 'Archive', tag: 'Warehouse' },
];

export const alertCards = [
  { title: 'Low Stock Alert', description: 'Steel billets in Warehouse 4 are below 30%.', icon: 'AlertTriangle', color: 'bg-amber-50 text-amber-900' },
  { title: 'Delayed Truck', description: 'Truck #17 has a 45-minute delay near the highway.', icon: 'Clock3', color: 'bg-rose-50 text-rose-900' },
  { title: 'Pending Payroll', description: 'Payroll approval pending for 220 employees.', icon: 'Wallet', color: 'bg-blue-50 text-blue-900' },
  { title: 'Invoice Due', description: '3 client invoices are overdue this week.', icon: 'CreditCard', color: 'bg-sky-50 text-sky-900' },
];

export const insights = [
  { title: 'Warehouse stock prediction', description: 'Inventory is expected to remain stable with a 12% buffer next month.' },
  { title: 'Delivery delay prediction', description: 'Peak traffic risk on route D12 may impact 6 deliveries tomorrow.' },
  { title: 'Cost optimization suggestion', description: 'Adjust fuel routes and vendor allocation to reduce logistics cost by 4%.' },
  { title: 'Demand forecast', description: 'Demand for hot-rolled steel is projected to rise by 8% in Q3.' },
];

export const chartData = {
  revenue: [
    { month: 'Jan', revenue: 120, expenses: 90 },
    { month: 'Feb', revenue: 135, expenses: 104 },
    { month: 'Mar', revenue: 155, expenses: 112 },
    { month: 'Apr', revenue: 160, expenses: 120 },
    { month: 'May', revenue: 178, expenses: 132 },
    { month: 'Jun', revenue: 192, expenses: 141 },
  ],
  delivery: [
    { month: 'Jan', deliveries: 92 },
    { month: 'Feb', deliveries: 106 },
    { month: 'Mar', deliveries: 125 },
    { month: 'Apr', deliveries: 118 },
    { month: 'May', deliveries: 142 },
    { month: 'Jun', deliveries: 163 },
  ],
  attendance: [
    { day: 'Mon', rate: 88 },
    { day: 'Tue', rate: 91 },
    { day: 'Wed', rate: 93 },
    { day: 'Thu', rate: 90 },
    { day: 'Fri', rate: 94 },
    { day: 'Sat', rate: 86 },
  ],
  warehouse: [
    { name: 'Raw Steel', value: 48 },
    { name: 'Finished Goods', value: 28 },
    { name: 'Tooling', value: 14 },
    { name: 'Spare Parts', value: 10 },
  ],
};

export const userProfile = {
  name: 'Rajesh Nair',
  role: 'Operations Head',
  location: 'Kolkata, India',
  avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=120&q=80',
};
