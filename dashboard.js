// Dashboard.js - Main React component for the productivity dashboard

// Constants for the dashboard
const COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
];

// Data Processors
function processProductivityData(rawData) {
    // Here we assume rawData is the JSON formatted data from our Python backend
    // In a real implementation, this would come from an API call to our backend
    return rawData;
}

// Format line chart data for time series
function prepareEmployeeTimeData(filteredData, selectedEmployee, dateRange) {
    // Get only top 10 employees by monthly average if no employee is selected
    let dataToDisplay = filteredData;
    
    if (!selectedEmployee) {
        dataToDisplay = _.orderBy(filteredData, ['monthlyAvg'], ['desc']).slice(0, 10);
    } else {
        dataToDisplay = filteredData.filter(emp => emp.email === selectedEmployee);
    }
    
    // Convert to the format needed for the line chart
    const chartData = [];
    for (let day = parseInt(dateRange.start); day <= parseInt(dateRange.end); day++) {
        const dayStr = day.toString().padStart(2, '0');
        const dataPoint = { date: `Mar ${dayStr}` };
        
        dataToDisplay.forEach(emp => {
            dataPoint[emp.name] = parseFloat(emp[dayStr]);
        });
        
        chartData.push(dataPoint);
    }
    
    return chartData;
}

// Distribution chart data
function prepareDistributionData(filteredData) {
    const distribution = [
        { range: '0.0-0.3', count: 0, color: '#e15759' },
        { range: '0.3-0.6', count: 0, color: '#f28e2c' },
        { range: '0.6-0.8', count: 0, color: '#4e79a7' },
        { range: '0.8-1.0', count: 0, color: '#59a14f' }
    ];
    
    filteredData.forEach(emp => {
        const value = parseFloat(emp.monthlyAvg);
        if (value < 0.3) distribution[0].count++;
        else if (value < 0.6) distribution[1].count++;
        else if (value < 0.8) distribution[2].count++;
        else distribution[3].count++;
    });
    
    return distribution;
}

// Daily average data
function calculateDailyAverages(data) {
    const dailyAverages = [];
    
    for (let day = 1; day <= 31; day++) {
        const dayStr = day.toString().padStart(2, '0');
        const dayAvg = data.reduce((sum, emp) => sum + parseFloat(emp[dayStr] || 0), 0) / (data.length || 1);
        
        dailyAverages.push({
            day: dayStr,
            date: `Mar ${dayStr}`,
            average: dayAvg.toFixed(2)
        });
    }
    
    return dailyAverages;
}

// Filter aggregated daily data based on date range
function prepareAggregateData(dailyAvgData, dateRange) {
    return dailyAvgData.filter(item => {
        const day = parseInt(item.day);
        return day >= parseInt(dateRange.start) && day <= parseInt(dateRange.end);
    });
}

// Radar chart data for individual employee activity
function prepareRadarData(activityData, selectedEmployee) {
    if (!selectedEmployee) return [];
    
    const employee = activityData.find(emp => emp.email === selectedEmployee);
    if (!employee) return [];
    
    const metrics = [
        'Sent emails', 'Email usage', 'File editing', 
        'File viewing', 'File adding', 'Chats', 
        'Meetings', 'Autodesk usage', 'VPN usage'
    ];
    
    return metrics.map(metric => ({
        subject: metric,
        value: parseFloat(employee[metric]),
        fullMark: 1
    }));
}

// Get employees with low connectivity
function getLowConnectivityEmployees(filteredData) {
    return filteredData
        .filter(emp => parseFloat(emp.monthlyAvg) < 0.3)
        .sort((a, b) => parseFloat(a.monthlyAvg) - parseFloat(b.monthlyAvg));
}

// Helper functions for extracting unique values for filters
function getUniqueValues(data, field) {
    return _.uniq(data.map(item => item[field]));
}

// Mock data generation based on the structure from calculate_productivity.py
function generateMockData() {
    // Mock employees with divisions and departments
    const divisions = ["DIRECCIÓN DE SUPERVISIÓN", "PRESIDENCIA", "DIVISIÓN ADMINISTRATIVA", "DIVISIÓN TECNOLOGÍA", "DIVISIÓN AMBIENTAL"];
    const departments = ["DPTO. DIRECCIÓN SUPERVISIÓN", "PROYECTOS DIRECCIÓN SUPER", "G/T. ITUANGO OBRAS PRINCIP", "DPTO. DIRECCIÓN PRESIDENCIA", "DPTO. SERVICIOS GENERALES", "DPTO. DATA SCIENCE", "DPTO. INGENIERÍA AMBIENT"];
    const categories = ["01", "02", "03", "04", "05", "06", "07", "C1"];
    
    const employees = [
        { name: "Manuel Francisco Villarraga Macias", email: "manuel.villarraga@ingetec.com.co", cat: "03", division: divisions[0], department: departments[0] },
        { name: "Juan José Saiz Cúlma", email: "juan.saiz@ingetec.com.co", cat: "06", division: divisions[0], department: departments[2] },
        { name: "Diana Marcela Ramirez Chaves", email: "diana.ramirez@ingetec.com.co", cat: "06", division: divisions[0], department: departments[2] },
        { name: "Elmy Gisela Real Garay", email: "elmy.real@ingetec.com.co", cat: "06", division: divisions[0], department: departments[0] },
        { name: "Diana Margarita Orjuela Vega", email: "diana.orjuela@ingetec.com.co", cat: "05", division: divisions[0], department: departments[1] },
        { name: "Christian David Pinzon Rincon", email: "christian.pinzon@ingetec.com.co", cat: "03", division: divisions[0], department: departments[0] },
        { name: "Laura Valentina Niño Guzman", email: "laura.nino@ingetec.com.co", cat: "05", division: divisions[0], department: departments[2] },
        { name: "Adriana Patricia Charry Hoyos", email: "adriana.charry@ingetec.com.co", cat: "06", division: divisions[0], department: departments[1] },
        { name: "Angela Johana Preciado Camacho", email: "angela.preciado@ingetec.com.co", cat: "C1", division: divisions[2], department: departments[4] },
        { name: "Carlos Mauricio Porras Rodriguez", email: "carlos.porras@ingetec.com.co", cat: "07", division: divisions[3], department: departments[5] },
        { name: "Oscar Javier Justinico Cardozo", email: "oscar.justinico@ingetec.com.co", cat: "06", division: divisions[0], department: departments[0] },
        { name: "Jennifer Cortes Henao", email: "jennifer.cortes@ingetec.com.co", cat: "06", division: divisions[0], department: departments[2] },
        { name: "Alberto Mariánda Posada", email: "alberto.miranda@ingetec.com.co", cat: "01", division: divisions[1], department: departments[3] },
        { name: "Maria Lucia Gomez Bohorquez", email: "maria.gomez@ingetec.com.co", cat: "05", division: divisions[0], department: departments[1] },
        { name: "Wilson Hernando Piña Avila", email: "wilson.pina@ingetec.com.co", cat: "06", division: divisions[0], department: departments[2] }
    ];

    // Generate daily productivity values for March 2025
    const days = [];
    for (let i = 1; i <= 31; i++) {
        days.push(i.toString().padStart(2, '0'));
    }

    const employeeData = employees.map(emp => {
        const dailyData = {};
        days.forEach(day => {
            // Create realistic productivity patterns (0.5-1.0 with some dips)
            const baseProd = Math.random() * 0.3 + 0.65;
            const weekendEffect = (parseInt(day) % 7 === 0 || parseInt(day) % 7 === 6) ? 0.6 : 1;
            const randomVariation = Math.random() * 0.2 - 0.1;
            
            // Add a realistic dip on some random days
            const randomDip = Math.random() > 0.9 ? 0.5 : 1;
            
            dailyData[day] = Math.min(1, Math.max(0, baseProd * weekendEffect * randomDip + randomVariation)).toFixed(2);
        });

        // Calculate monthly average
        const monthlyAvg = Object.values(dailyData).reduce((sum, val) => sum + parseFloat(val), 0) / days.length;

        return {
            ...emp,
            ...dailyData,
            monthlyAvg: monthlyAvg.toFixed(2)
        };
    });

    return employeeData;
}

// Generate activity metrics for radar chart
function generateActivityData(employeeData) {
    const activityMetrics = [
        'Sent emails', 'Email usage', 'File editing', 
        'File viewing', 'File adding', 'Chats', 
        'Meetings', 'Autodesk usage', 'VPN usage'
    ];
    
    return employeeData.map(emp => {
        const activities = {};
        activityMetrics.forEach(metric => {
            // Generate different patterns based on employee category
            let baseValue;
            if (emp.cat === "06" || emp.cat === "07") {
                baseValue = Math.random() * 0.4 + 0.5; // Higher base for these categories
            } else if (emp.cat === "01" || emp.cat === "02") {
                baseValue = Math.random() * 0.5 + 0.4; // Medium base
            } else {
                baseValue = Math.random() * 0.5 + 0.3; // Lower base
            }
            
            // Add some category-specific patterns
            if ((emp.cat === "06" || emp.cat === "07") && metric === 'Autodesk usage') {
                activities[metric] = (baseValue * 1.4).toFixed(2);
            } else if ((emp.cat === "01" || emp.cat === "02") && metric === 'Meetings') {
                activities[metric] = (baseValue * 1.3).toFixed(2);
            } else if (metric === 'VPN usage') {
                activities[metric] = (baseValue * 0.8).toFixed(2);
            } else {
                activities[metric] = baseValue.toFixed(2);
            }
        });
        
        return {
            name: emp.name,
            email: emp.email,
            cat: emp.cat,
            ...activities
        };
    });
}

// Define the application component structure
function ProductivityDashboard() {
    // Generate mock data for demonstration
    const employeeData = generateMockData();
    const activityData = generateActivityData(employeeData);
    
    // State initialization
    const [filteredData, setFilteredData] = React.useState(employeeData);
    const [dailyAvgData, setDailyAvgData] = React.useState(calculateDailyAverages(employeeData));
    const [selectedDivision, setSelectedDivision] = React.useState('All');
    const [selectedDepartment, setSelectedDepartment] = React.useState('All');
    const [selectedCategory, setSelectedCategory] = React.useState('All');
    const [selectedEmployee, setSelectedEmployee] = React.useState(null);
    const [dateRange, setDateRange] = React.useState({ start: '01', end: '31' });
    
    // Filter data based on selections
    React.useEffect(() => {
        let filtered = [...employeeData];
        
        if (selectedDivision !== 'All') {
            filtered = filtered.filter(emp => emp.division === selectedDivision);
        }
        
        if (selectedDepartment !== 'All') {
            filtered = filtered.filter(emp => emp.department === selectedDepartment);
        }
        
        if (selectedCategory !== 'All') {
            filtered = filtered.filter(emp => emp.cat === selectedCategory);
        }
        
        setFilteredData(filtered);
    }, [selectedDivision, selectedDepartment, selectedCategory]);
    
    // Update daily averages when filtered data changes
    React.useEffect(() => {
        setDailyAvgData(calculateDailyAverages(filteredData));
    }, [filteredData]);
    
    // Get unique values for filters
    const divisions = getUniqueValues(employeeData, 'division');
    const departments = getUniqueValues(employeeData, 'department');
    const categories = getUniqueValues(employeeData, 'cat');
    
    // Render the dashboard
    return (
        <div className="flex flex-col bg-gray-50 min-h-screen">
            {/* Header */}
            <div className="dashboard-header flex items-center justify-between">
                <div className="flex items-center">
                    <div className="company-logo">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M12 2v4m0 12v4M4.93 4.93l2.83 2.83m8.48 8.48l2.83 2.83M2 12h4m12 0h4M4.93 19.07l2.83-2.83m8.48-8.48l2.83-2.83" />
                        </svg>
                    </div>
                    <div>
                        <h1 className="header-title">Productividad Avanzada</h1>
                        <p className="header-subtitle">Marzo 2025</p>
                    </div>
                </div>
                <div className="flex space-x-1">
                    <button className="header-button">Exportar PDF</button>
                    <button className="header-button">Exportar Excel</button>
                </div>
            </div>

            {/* Filters */}
            <div className="filters-container">
                <div className="grid md:grid-cols-5 gap-4">
                    <div>
                        <label className="filter-label">División</label>
                        <select 
                            className="filter-select" 
                            value={selectedDivision}
                            onChange={e => setSelectedDivision(e.target.value)}
                        >
                            <option value="All">Todas las divisiones</option>
                            {divisions.map((div, idx) => (
                                <option key={idx} value={div}>{div}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="filter-label">Departamento</label>
                        <select 
                            className="filter-select"
                            value={selectedDepartment}
                            onChange={e => setSelectedDepartment(e.target.value)}
                        >
                            <option value="All">Todos los departamentos</option>
                            {departments.map((dept, idx) => (
                                <option key={idx} value={dept}>{dept}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="filter-label">Categoría</label>
                        <select 
                            className="filter-select"
                            value={selectedCategory}
                            onChange={e => setSelectedCategory(e.target.value)}
                        >
                            <option value="All">Todas las categorías</option>
                            {categories.map((cat, idx) => (
                                <option key={idx} value={cat}>{cat}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="filter-label">Empleado</label>
                        <select 
                            className="filter-select"
                            value={selectedEmployee || ''}
                            onChange={e => setSelectedEmployee(e.target.value || null)}
                        >
                            <option value="">Todos los empleados</option>
                            {filteredData.map((emp, idx) => (
                                <option key={idx} value={emp.email}>{emp.name}</option>
                            ))}
                        </select>
                    </div>
                    <div>
                        <label className="filter-label">Rango de Fechas</label>
                        <div className="flex items-center">
                            <select 
                                className="w-1/2 border border-gray-300 rounded-l-md p-2 text-sm"
                                value={dateRange.start}
                                onChange={e => setDateRange({...dateRange, start: e.target.value})}
                            >
                                {Array.from({length: 31}, (_, i) => (i + 1).toString().padStart(2, '0')).map(day => (
                                    <option key={day} value={day}>{day}</option>
                                ))}
                            </select>
                            <span className="mx-1">-</span>
                            <select 
                                className="w-1/2 border border-gray-300 rounded-r-md p-2 text-sm"
                                value={dateRange.end}
                                onChange={e => setDateRange({...dateRange, end: e.target.value})}
                            >
                                {Array.from({length: 31}, (_, i) => (i + 1).toString().padStart(2, '0')).map(day => (
                                    <option key={day} value={day}>{day}</option>
                                ))}
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main Content - Charts */}
            <div className="p-4 grid md:grid-cols-3 gap-4">
                {/* Productivity Over Time Chart */}
                <div className="md:col-span-2 chart-card">
                    <h2 className="chart-title">Control Diario de Productividad (Marzo 2025)</h2>
                    <div className="chart-container">
                        <Recharts.ResponsiveContainer width="100%" height="100%">
                            <Recharts.LineChart
                                data={prepareEmployeeTimeData(filteredData, selectedEmployee, dateRange)}
                                margin={{ top: 5, right: 30, left: 10, bottom: 5 }}
                            >
                                <Recharts.CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                                <Recharts.XAxis dataKey="date" />
                                <Recharts.YAxis domain={[0, 1]} />
                                <Recharts.Tooltip />
                                <Recharts.Legend />
                                {selectedEmployee ? (
                                    <Recharts.Line 
                                        type="monotone" 
                                        dataKey={filteredData.find(emp => emp.email === selectedEmployee)?.name || ''} 
                                        stroke="#8884d8" 
                                        strokeWidth={3}
                                        dot={{ stroke: '#8884d8', strokeWidth: 2, r: 4 }}
                                        activeDot={{ r: 8 }}
                                    />
                                ) : (
                                    _.orderBy(filteredData, ['monthlyAvg'], ['desc'])
                                        .slice(0, 10)
                                        .map((emp, idx) => (
                                            <Recharts.Line 
                                                key={emp.email}
                                                type="monotone"
                                                dataKey={emp.name}
                                                stroke={COLORS[idx % COLORS.length]}
                                                dot={{ stroke: COLORS[idx % COLORS.length], strokeWidth: 1, r: 3 }}
                                            />
                                        ))
                                )}
                            </Recharts.LineChart>
                        </Recharts.ResponsiveContainer>
                    </div>
                </div>

                {/* Distribution Chart */}
                <div className="chart-card">
                    <h2 className="chart-title">Distribución de Productividad</h2>
                    <div className="chart-container">
                        <Recharts.ResponsiveContainer width="100%" height="100%">
                            <Recharts.PieChart>
                                <Recharts.Pie
                                    data={prepareDistributionData(filteredData)}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={true}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    dataKey="count"
                                    nameKey="range"
                                    label={({range, count, percent}) => `${range}: ${count} (${(percent * 100).toFixed(0)}%)`}
                                >
                                    {prepareDistributionData(filteredData).map((entry, index) => (
                                        <Recharts.Cell key={`cell-${index}`} fill={entry.color} />
                                    ))}
                                </Recharts.Pie>
                                <Recharts.Tooltip />
                            </Recharts.PieChart>
                        </Recharts.ResponsiveContainer>
                    </div>
                </div>

                {/* Average Productivity Area Chart */}
                <div className="chart-card">
                    <h2 className="chart-title">Productividad Media Diaria</h2>
                    <div className="chart-container">
                        <Recharts.ResponsiveContainer width="100%" height="100%">
                            <Recharts.AreaChart
                                data={prepareAggregateData(dailyAvgData, dateRange)}
                                margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                            >
                                <defs>
                                    <linearGradient id="colorAvg" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                                        <stop offset="95%" stopColor="#8884d8" stopOpacity={0.1}/>
                                    </linearGradient>
                                </defs>
                                <Recharts.CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                                <Recharts.XAxis dataKey="date" />
                                <Recharts.YAxis domain={[0, 1]} />
                                <Recharts.Tooltip />
                                <Recharts.Area 
                                    type="monotone" 
                                    dataKey="average" 
                                    stroke="#8884d8" 
                                    fillOpacity={1} 
                                    fill="url(#colorAvg)" 
                                />
                            </Recharts.AreaChart>
                        </Recharts.ResponsiveContainer>
                    </div>
                </div>

                {/* Activity Breakdown for Selected Employee */}
                <div className="chart-card">
                    <h2 className="chart-title">
                        {selectedEmployee ? 
                            `Desglose de Actividad: ${filteredData.find(emp => emp.email === selectedEmployee)?.name}` : 
                            'Seleccione un empleado para ver el desglose de actividad'}
                    </h2>
                    <div className="chart-container">
                        {selectedEmployee ? (
                            <Recharts.ResponsiveContainer width="100%" height="100%">
                                <Recharts.RadarChart outerRadius={80} data={prepareRadarData(activityData, selectedEmployee)}>
                                    <Recharts.PolarGrid stroke="#e5e7eb" />
                                    <Recharts.PolarAngleAxis dataKey="subject" tick={{ fontSize: 10 }} />
                                    <Recharts.PolarRadiusAxis domain={[0, 1]} />
                                    <Recharts.Radar
                                        name="Actividad"
                                        dataKey="value"
                                        stroke="#8884d8"
                                        fill="#8884d8"
                                        fillOpacity={0.6}
                                    />
                                    <Recharts.Tooltip />
                                </Recharts.RadarChart>
                            </Recharts.ResponsiveContainer>
                        ) : (
                            <div className="empty-state">
                                <svg xmlns="http://www.w3.org/2000/svg" className="empty-state-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                                </svg>
                                <p>Seleccione un empleado para ver el análisis detallado</p>
                            </div>
                        )}
                    </div>
                </div>
                
                {/* Productivity by Category */}
                <div className="chart-card">
                    <h2 className="chart-title">Productividad por Categoría</h2>
                    <div className="chart-container">
                        <Recharts.ResponsiveContainer width="100%" height="100%">
                            <Recharts.BarChart
                                data={_.chain(filteredData)
                                    .groupBy('cat')
                                    .map((group, cat) => ({
                                        cat,
                                        average: (_.sumBy(group, emp => parseFloat(emp.monthlyAvg)) / group.length).toFixed(2),
                                        count: group.length
                                    }))
                                    .value()
                                    .sort((a, b) => parseFloat(b.average) - parseFloat(a.average))
                                }
                                margin={{ top: 5, right: 30, left: 10, bottom: 5 }}
                            >
                                <Recharts.CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                                <Recharts.XAxis dataKey="cat" />
                                <Recharts.YAxis domain={[0, 1]} />
                                <Recharts.Tooltip />
                                <Recharts.Legend />
                                <Recharts.Bar dataKey="average" name="Productividad Media" fill="#4e79a7" />
                            </Recharts.BarChart>
                        </Recharts.ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Tables Section */}
            <div className="p-4 grid md:grid-cols-2 gap-4">
                {/* Monthly Average Table */}
                <div className="chart-card">
                    <h2 className="chart-title">Promedio mensual conectividad por empleado</h2>
                    <div className="table-container">
                        <table className="data-table">
                            <thead className="table-header">
                                <tr>
                                    <th>Empleado</th>
                                    <th>Cat</th>
                                    <th>Promedio Marzo 2025</th>
                                </tr>
                            </thead>
                            <tbody className="table-body">
                                {_.orderBy(filteredData, ['monthlyAvg'], ['desc']).slice(0, 10).map((employee, idx) => (
                                    <tr key={employee.email} className={idx % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                                        <td className="table-cell cell-name">{employee.name}</td>
                                        <td className="table-cell cell-normal">{employee.cat}</td>
                                        <td className="table-cell cell-normal">
                                            <div className="progress-container">
                                                <span className="progress-value">{employee.monthlyAvg}</span>
                                                <div className="progress-bar-bg">
                                                    <div 
                                                        className={`progress-bar ${
                                                            parseFloat(employee.monthlyAvg) >= 0.8 ? 'progress-high' : 
                                                            parseFloat(employee.monthlyAvg) >= 0.6 ? 'progress-medium' : 
                                                            parseFloat(employee.monthlyAvg) >= 0.3 ? 'progress-low' : 'progress-critical'
                                                        }`} 
                                                        style={{ width: `${parseFloat(employee.monthlyAvg) * 100}%` }}
                                                    ></div>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Low Connectivity Employees */}
                <div className="chart-card">
                    <h2 className="chart-title">Empleados con conectividad menor a 30%</h2>
                    <div className="table-container">
                        <table className="data-table">
                            <thead className="table-header">
                                <tr>
                                    <th>Empleado</th>
                                    <th>Cat</th>
                                    <th>División</th>
                                    <th>Departamento</th>
                                    <th>Productividad</th>
                                </tr>
                            </thead>
                            <tbody className="table-body">
                                {getLowConnectivityEmployees(filteredData).map((employee, idx) => (
                                    <tr key={employee.email} className="low-connectivity">
                                        <td className="table-cell cell-name">{employee.name}</td>
                                        <td className="table-cell cell-normal">{employee.cat}</td>
                                        <td className="table-cell cell-normal">{employee.division}</td>
                                        <td className="table-cell cell-normal">{employee.department}</td>
                                        <td className="table-cell cell-alert">{employee.monthlyAvg}</td>
                                    </tr>
                                ))}
                                {getLowConnectivityEmployees(filteredData).length === 0 && (
                                    <tr>
                                        <td colSpan={5} className="table-cell text-center">
                                            No hay empleados con conectividad menor a 30%
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    ReactDOM.render(
        React.createElement(ProductivityDashboard),
        document.getElementById('root')
    );
});