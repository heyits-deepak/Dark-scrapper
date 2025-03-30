import React from "react";
import { Bar, Pie, Radar, Bubble } from "react-chartjs-2";
import {
    Chart as ChartJS,
    LineElement,
    BarElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    RadialLinearScale
} from "chart.js";

// Register the required elements
ChartJS.register(
    LineElement,
    BarElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    RadialLinearScale
);

const SummaryBarChart = ({ jsonData, options, refresh }) => {
    const data = {
        labels: ["Emails", "Credentials", "IPs", "Domains", "Credit Cards"],
        datasets: [
            {
                label: "Total Leaks",
                data: Object.values(jsonData.summary),
                backgroundColor: [
                    "rgba(17, 93, 119, 0.8)",  // Deep Teal
                    "rgba(17, 119, 107, 0.8)", // Greenish Teal
                    "rgba(64, 224, 208, 0.8)", // Turquoise
                    "rgba(37, 184, 238, 0.8)", // Sky Blue
                    "rgba(17, 119, 171, 0.8)"  // Deep Blue-Teal
                ],
                borderColor: "transparent",
                borderWidth: 1,
                hoverBackgroundColor: [
                    "rgba(17, 93, 119, 1)",
                    "rgba(17, 119, 107, 1)",
                    "rgba(64, 224, 208, 1)",
                    "rgba(37, 184, 238, 1)",
                    "rgba(17, 119, 171, 1)"
                ],
                borderRadius: 5, // Rounded bars for smoothness
                barPercentage: 0.8,
            }
        ]
    };

    return (
        <div className="w-full h-full flex justify-center items-start">
            <Bar data={data} options={options} key={refresh} />
        </div>
    );
};

const ThreatsPieChart = ({ jsonData, options, refresh }) => {
    const threatsCount = Object.keys(jsonData.threats).length;
    const safeCount = jsonData.summary.total_domains - threatsCount;

    const data = {
        labels: ["Threat Domains", "Safe Domains"],
        datasets: [
            {
                data: [threatsCount, safeCount],
                backgroundColor: [
                    "rgba(17, 119, 171, 0.8)",  // Deep Teal
                    "rgba(64, 224, 208, 0.8)", // Turquoise
                ],
                borderColor: "transparent",
                hoverBackgroundColor: [
                    "rgba(17, 119, 171, 1)",
                    "rgba(64, 224, 208, 1)"
                ],
                hoverOffset: 7,
            }
        ]
    };

    return (
        <div className="w-full h-full flex justify-center items-start">
            <Pie data={data} options={options} key={refresh} />
        </div>
    );
};

const LeaksRadarChart = ({ jsonData, options, refresh }) => {
    const data = {
        labels: ["Emails", "Credentials", "IPs", "Domains", "Credit Cards"],
        datasets: [
            {
                label: "Leaks",
                data: [
                    jsonData.leaks.emails.length,
                    jsonData.leaks.credentials.length,
                    jsonData.leaks.ip_addresses.length,
                    jsonData.leaks.domains.length,
                    jsonData.leaks.credit_cards.length
                ],
                backgroundColor: "rgba(64, 224, 208, 0.3)", // Transparent Turquoise
                borderColor: "rgba(17, 93, 119, 1)", // Deep Teal
                borderWidth: 2,
                pointBackgroundColor: "white",
                pointBorderColor: "rgba(17, 93, 119, 1)",
                pointHoverRadius: 7,
            }
        ]
    };

    return (
        <div className="w-full h-full flex justify-center items-start">
            <Radar data={data} options={options} key={refresh} />
        </div>
    );
};

const ThreatBubbleChart = ({ jsonData, options, refresh }) => {
    const data = {
        datasets: [
            {
                label: "Threats",
                data: Object.keys(jsonData.threats).map((domain, index) => ({
                    x: index,
                    y: 1,
                    r: 10
                })),
                backgroundColor: "rgba(37, 184, 238, 0.8)", // Light teal
            }
        ]
    };

    return (
        <div className="w-full h-full flex justify-center items-start">
            <Bubble data={data} options={options} key={refresh} />
        </div>
    );
};


const Visualization = ({data, moveInput}) => {
    const options = {
        responsive: true,
        // maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: "white", // Legend text color
                },
            },
        },
        scales: {
            x: { grid: {display: false},
                ticks: { color: "white" }, // X-axis labels color
            },
            y: { grid: {display: false},
                ticks: { color: "white" }, 
            },
        },
    };

    const radarOptions = {
        ...options,
        scales: {
            r: {
                grid: { display: false },
                angleLines: { color: "rgba(141, 210, 235, 0.489)" },
                ticks: { color: "white", backdropColor: "transparent", font: "bold" },
                pointLabels: { color: "white" },
            },
        },
    };

  return (
    <div className={`w-[95%] md:w-[85%] h-[60vh] md:h-[70%] overflow-auto p-4 grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-6 
        ${moveInput ? 'fade-in': 'fade-out'}`}>
        
        <div className="bg-[#0f2b34cc] shadow-md shadow-teal-700 p-4 rounded-lg text-center">
            <h2 className="text-teal-400 text-lg font-semibold uppercase">📊 Data Breach Overview</h2>
            <SummaryBarChart jsonData={data} options={options} refresh={moveInput}/>
      </div>
      <div className="bg-[#0f2b34cc] shadow-md shadow-teal-700 p-4 rounded-lg text-center">
            <h2 className="text-teal-400 text-lg font-semibold uppercase">🔍 Real-Time Threat Analysis</h2>
            <ThreatBubbleChart jsonData={data} options={options} refresh={moveInput}/>
      </div>
      <div className="bg-[#0f2b34cc] shadow-md shadow-teal-700 p-4 rounded-lg text-center">
            <h2 className="text-teal-400 text-lg font-semibold uppercase">🚨 Threat Intelligence Insights</h2>
            <ThreatsPieChart jsonData={data} options={options} refresh={moveInput}/>
      </div>
      <div className="bg-[#0f2b34cc] shadow-md shadow-teal-700 p-4 rounded-lg text-center">
            <h2 className="text-teal-400 text-lg font-semibold uppercase">🔓 Compromised Data Breakdown</h2>
            <LeaksRadarChart jsonData={data} options={radarOptions} refresh={moveInput}/>
      </div>
        
    </div>
  )
}

export default Visualization