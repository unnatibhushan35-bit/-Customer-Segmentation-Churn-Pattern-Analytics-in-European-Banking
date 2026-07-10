import React from "react";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, AreaChart, Area
} from "recharts";
import { 
  Users, AlertTriangle, DollarSign, Activity, 
  MapPin, Clock, Award, ShieldAlert 
} from "lucide-react";
import { CustomerRecord } from "../data/churnData";
import { FilterState } from "../types";

interface DashboardOverviewProps {
  filteredData: CustomerRecord[];
  allData: CustomerRecord[];
  filters: FilterState;
  setFilters: React.Dispatch<React.SetStateAction<FilterState>>;
}

const COLORS = ["#2563eb", "#ef4444", "#10b981", "#f59e0b", "#6366f1", "#8b5cf6"];

export const DashboardOverview: React.FC<DashboardOverviewProps> = ({
  filteredData,
  allData,
  filters,
  setFilters
}) => {
  // 1. KPI Calculations based on filtered data
  const totalCustomers = filteredData.length;
  const churnedCustomers = filteredData.filter(d => d.exited).length;
  const overallChurnRate = totalCustomers > 0 ? (churnedCustomers / totalCustomers) * 100 : 0;

  // High Value Churn (Premium customers: Balance > $100,000)
  const premiumCustomers = filteredData.filter(d => d.balance > 100000);
  const premiumChurned = premiumCustomers.filter(d => d.exited).length;
  const highValueChurnRatio = premiumCustomers.length > 0 ? (premiumChurned / premiumCustomers.length) * 100 : 0;

  // Revenue At Risk
  const totalRevenueAtRisk = filteredData.filter(d => d.exited).reduce((sum, curr) => sum + curr.balance, 0);

  // Engagement Drop: Active Churn vs Inactive Churn
  const activeCustomers = filteredData.filter(d => d.isActiveMember);
  const activeChurnRate = activeCustomers.length > 0 
    ? (activeCustomers.filter(d => d.exited).length / activeCustomers.length) * 100 
    : 0;

  const inactiveCustomers = filteredData.filter(d => !d.isActiveMember);
  const inactiveChurnRate = inactiveCustomers.length > 0 
    ? (inactiveCustomers.filter(d => d.exited).length / inactiveCustomers.length) * 100 
    : 0;

  // 2. Geographic Segmentation Analysis
  const geoStats = ["France", "Spain", "Germany"].map(geo => {
    const geoData = filteredData.filter(d => d.geography === geo);
    const total = geoData.length;
    const churned = geoData.filter(d => d.exited).length;
    const rate = total > 0 ? (churned / total) * 100 : 0;
    const avgBalance = total > 0 ? geoData.reduce((sum, curr) => sum + curr.balance, 0) / total : 0;
    return { name: geo, Total: total, Churned: churned, "Churn Rate (%)": parseFloat(rate.toFixed(1)), "Avg Balance ($)": Math.round(avgBalance) };
  });

  // 3. Age Brackets Segment Analysis
  // <30, 30–45, 46–60, 60+
  const getAgeBracket = (age: number) => {
    if (age < 30) return "<30";
    if (age <= 45) return "30-45";
    if (age <= 60) return "46-60";
    return "60+";
  };

  const ageBrackets = ["<30", "30-45", "46-60", "60+"];
  const ageStats = ageBrackets.map(bracket => {
    const ageData = filteredData.filter(d => getAgeBracket(d.age) === bracket);
    const total = ageData.length;
    const churned = ageData.filter(d => d.exited).length;
    const rate = total > 0 ? (churned / total) * 100 : 0;
    return { name: bracket, Total: total, Churned: churned, "Churn Rate (%)": parseFloat(rate.toFixed(1)) };
  });

  // 4. Tenure Segments Analysis
  // New (0-2), Mid-term (3-7), Long-term (8-10)
  const getTenureGroup = (tenure: number) => {
    if (tenure <= 2) return "New (0-2 yrs)";
    if (tenure <= 7) return "Mid-term (3-7 yrs)";
    return "Long-term (8-10 yrs)";
  };

  const tenureGroups = ["New (0-2 yrs)", "Mid-term (3-7 yrs)", "Long-term (8-10 yrs)"];
  const tenureStats = tenureGroups.map(group => {
    const tenureData = filteredData.filter(d => getTenureGroup(d.tenure) === group);
    const total = tenureData.length;
    const churned = tenureData.filter(d => d.exited).length;
    const rate = total > 0 ? (churned / total) * 100 : 0;
    return { name: group, Total: total, Churned: churned, "Churn Rate (%)": parseFloat(rate.toFixed(1)) };
  });

  // 5. Active vs Inactive Churn Pie Chart Data
  const engagementStats = [
    { name: "Active Members", value: Math.round(activeChurnRate), count: activeCustomers.filter(d => d.exited).length },
    { name: "Inactive Members", value: Math.round(inactiveChurnRate), count: inactiveCustomers.filter(d => d.exited).length }
  ];

  // Quick reset filters helper
  const handleResetFilters = () => {
    setFilters({
      geography: [],
      gender: [],
      creditScoreBand: [],
      tenureGroup: [],
      balanceSegment: [],
      isActiveMember: []
    });
  };

  return (
    <div className="space-y-6" id="dashboard-tab">
      {/* Dynamic Objectives Header Matrix */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
          <Award className="w-5 h-5 text-blue-600 animate-pulse" />
          <h3 className="font-extrabold text-slate-900 text-sm tracking-tight uppercase">Analytical Mandates & Objectives</h3>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-3.5 rounded-xl bg-blue-50/50 border border-blue-100/50 flex flex-col justify-between">
            <div>
              <span className="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-100 text-blue-700 uppercase tracking-wider mb-2">Primary Mandate</span>
              <p className="text-xs font-semibold text-slate-800">Measure Baseline Churn Rate</p>
              <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">Establish total banking portfolio risk exposure. Target population benchmark verified at exactly <strong className="text-blue-700">20.37%</strong>.</p>
            </div>
            <div className="mt-3 pt-2 border-t border-blue-100/30 flex items-center justify-between text-[11px]">
              <span className="text-slate-400 font-medium font-mono">Current Status:</span>
              <span className="font-extrabold text-blue-700 font-mono flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-pulse"></span>
                {overallChurnRate.toFixed(2)}% Calculated
              </span>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50/50 border border-slate-200/50 flex flex-col justify-between">
            <div>
              <span className="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-200/60 text-slate-700 uppercase tracking-wider mb-2">Secondary Mandate A</span>
              <p className="text-xs font-semibold text-slate-800">Geographic & Demographic Segments</p>
              <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">Identify regional hotspots (Germany vs France vs Spain), age bracket clusters, and tenure brackets.</p>
            </div>
            <div className="mt-3 pt-2 border-t border-slate-200/30 flex items-center justify-between text-[11px]">
              <span className="text-slate-400 font-medium font-mono">Analysis Scope:</span>
              <span className="font-bold text-slate-700 font-mono">Multi-country Risk Vector</span>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50/50 border border-slate-200/50 flex flex-col justify-between">
            <div>
              <span className="inline-block px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-200/60 text-slate-700 uppercase tracking-wider mb-2">Secondary Mandate B</span>
              <p className="text-xs font-semibold text-slate-800">Quantify Premium Portfolio Risk</p>
              <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">Assess balance flight on premium accounts (&gt;$100,000) to secure high-net-worth customers.</p>
            </div>
            <div className="mt-3 pt-2 border-t border-slate-200/30 flex items-center justify-between text-[11px]">
              <span className="text-slate-400 font-medium font-mono">Premium Exposure:</span>
              <span className="font-bold text-emerald-600 font-mono">${totalRevenueAtRisk.toLocaleString()}</span>
            </div>
          </div>
        </div>
      </div>

      {/* KPI Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* KPI 1: Overall Churn Rate */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow duration-200">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-500">Overall Churn Rate</span>
            <div className="p-2 bg-blue-50 rounded-xl text-blue-600">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <h3 className="text-3xl font-bold text-slate-900 tracking-tight">
              {overallChurnRate.toFixed(2)}%
            </h3>
            <p className="text-xs text-slate-400 mt-1 font-mono">
              {churnedCustomers} exited out of {totalCustomers} customers
            </p>
          </div>
        </div>

        {/* KPI 2: High Value Churn Ratio */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow duration-200">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-500">High-Value Churn</span>
            <div className="p-2 bg-blue-50 rounded-xl text-blue-600">
              <Award className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <h3 className="text-3xl font-bold text-slate-900 tracking-tight">
              {highValueChurnRatio.toFixed(2)}%
            </h3>
            <p className="text-xs text-slate-400 mt-1 font-mono">
              {premiumChurned} out of {premiumCustomers.length} accounts (&gt;$100k)
            </p>
          </div>
        </div>

        {/* KPI 3: Revenue At Risk */}
        <div className="rounded-2xl border border-blue-100 bg-blue-600 p-5 shadow-lg shadow-blue-200 flex flex-col justify-between hover:shadow-xl transition-shadow duration-200">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-blue-100">Total Revenue At Risk</span>
            <div className="p-2 bg-blue-500/30 rounded-xl text-white">
              <DollarSign className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <h3 className="text-3xl font-bold text-white tracking-tight">
              ${totalRevenueAtRisk.toLocaleString()}
            </h3>
            <p className="text-[10px] text-blue-200 mt-1 font-mono">
              Aggregated balances of lost accounts
            </p>
          </div>
        </div>

        {/* KPI 4: Inactivity Risk Indicator */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow duration-200">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-500">Inactivity Churn Risk</span>
            <div className="p-2 bg-red-50 rounded-xl text-red-600">
              <AlertTriangle className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <h3 className="text-3xl font-bold text-slate-900 tracking-tight">
              {inactiveChurnRate > 0 ? (inactiveChurnRate / (activeChurnRate || 1)).toFixed(1) : 0}x
            </h3>
            <p className="text-xs text-slate-400 mt-1 font-mono">
              Inactive: {inactiveChurnRate.toFixed(1)}% vs Active: {activeChurnRate.toFixed(1)}%
            </p>
          </div>
        </div>
      </div>

      {/* Visual Analytics Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Geography Wise Churn Visualization */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h4 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <MapPin className="w-5 h-5 text-blue-600" />
                Geographical Risk Analysis
              </h4>
              <p className="text-xs text-slate-500">Churn exposure and average account balances across Europe</p>
            </div>
          </div>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={geoStats} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#fff", borderRadius: "12px", border: "1px solid #e2e8f0", boxShadow: "0 10px 15px -3px rgba(0,0,0,0.05)" }}
                  formatter={(value: any, name: any) => [name === "Avg Balance ($)" ? `$${value.toLocaleString()}` : `${value}%`, name]}
                />
                <Legend iconType="circle" />
                <Bar dataKey="Churn Rate (%)" fill="#ef4444" radius={[4, 4, 0, 0]} maxBarSize={45} />
                <Bar dataKey="Avg Balance ($)" fill="#2563eb" radius={[4, 4, 0, 0]} maxBarSize={45} yAxisId={0} hide={filteredData.length === 0} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Age Segmentation Analysis */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h4 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Clock className="w-5 h-5 text-blue-600" />
                Age Bracket Segmentation
              </h4>
              <p className="text-xs text-slate-500">Granular churn trend across generational segments</p>
            </div>
          </div>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={ageStats} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                <defs>
                  <linearGradient id="colorAge" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.2}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: "#fff", borderRadius: "12px", border: "1px solid #e2e8f0" }} />
                <Legend iconType="circle" />
                <Area type="monotone" dataKey="Churn Rate (%)" stroke="#ef4444" fillOpacity={1} fill="url(#colorAge)" strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Tenure & Engagement Grid */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h4 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Activity className="w-5 h-5 text-blue-600" />
                Tenure Groups Analysis
              </h4>
              <p className="text-xs text-slate-500">Understanding years with the bank vs. exited rates</p>
            </div>
          </div>
          <div className="h-[280px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={tenureStats} margin={{ top: 10, right: 10, left: -20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="name" stroke="#64748b" fontSize={12} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: "#fff", borderRadius: "12px", border: "1px solid #e2e8f0" }} />
                <Legend iconType="circle" />
                <Line type="monotone" dataKey="Churn Rate (%)" stroke="#10b981" strokeWidth={3} dot={{ r: 6 }} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Engagement Drop (Active vs Inactive) */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h4 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <ShieldAlert className="w-5 h-5 text-blue-600" />
                Engagement & Inactivity Risk
              </h4>
              <p className="text-xs text-slate-500">Correlating active membership status with churn probability</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
            <div className="h-[200px] flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={engagementStats}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {engagementStats.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: "#fff", borderRadius: "12px", border: "1px solid #e2e8f0" }} formatter={(value) => `${value}%`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 rounded-full bg-blue-600 shrink-0" />
                <div>
                  <p className="text-sm font-semibold text-slate-700">Active Member Churn</p>
                  <p className="text-xs text-slate-500 font-mono">{activeChurnRate.toFixed(1)}% Churn Rate</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 rounded-full bg-red-500 shrink-0" />
                <div>
                  <p className="text-sm font-semibold text-slate-700">Inactive Member Churn</p>
                  <p className="text-xs text-slate-500 font-mono">{inactiveChurnRate.toFixed(1)}% Churn Rate</p>
                </div>
              </div>
              <div className="bg-amber-50/50 border border-amber-100 rounded-xl p-3 text-xs text-amber-800">
                ⚠️ **Strategic Insight:** Inactive members churn at a significantly higher rate. Activating customers via tailored deposit schemes or credit cards is highly recommended.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
