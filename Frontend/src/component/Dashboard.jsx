import React, { useEffect, useState } from "react";

const Dashboard = ({ data, moveInput }) => {
  const [counts, setCounts] = useState({
    emails: 0,
    credentials: 0,
    ips: 0,
    domains: 0,
    creditCards: 0,
  });

  useEffect(() => {
    if (!moveInput) return;

    const targetCounts = {
      emails: data.summary.total_emails,
      credentials: data.summary.total_credentials,
      ips: data.summary.total_ips,
      domains: data.summary.total_domains,
      creditCards: data.summary.total_credit_cards,
    };

    // Reset counts to zero before starting animation
    setCounts({
      emails: 0,
      credentials: 0,
      ips: 0,
      domains: 0,
      creditCards: 0,
    });

    let interval = setInterval(() => {
      setCounts((prev) => {
        let updated = {};
        let allReached = true;

        Object.keys(targetCounts).forEach((key) => {
          if (prev[key] < targetCounts[key]) {
            updated[key] = prev[key] + 1;
            allReached = false;
          } else {
            updated[key] = targetCounts[key];
          }
        });

        if (allReached) clearInterval(interval);
        return updated;
      });
    }, 100);

    return () => clearInterval(interval);
  }, [data, moveInput]);

  return (
    <div className={`w-[95%] md:w-[85%] p-4 grid grid-cols-2 md:grid-cols-5 gap-4 
        ${moveInput ? 'fade-in': 'fade-out'}`}>
      
      <div className="bg-[#0f2b34cc] shadow-md shadow-teal-700 p-4 rounded-lg text-center">
        <h3 className="text-gray-300 text-lg font-semibold">Emails</h3>
        <p className="text-teal-400 text-2xl md:text-5xl font-semibold">
          {counts.emails}
        </p>
      </div>
      
      <div className="bg-[#0f2b34cc] shadow-md shadow-teal-700 p-4 rounded-lg text-center">
        <h3 className="text-gray-300 text-lg font-semibold">Credentials</h3>
        <p className="text-teal-400 text-2xl md:text-5xl font-semibold">
          {counts.credentials}
        </p>
      </div>
      
      <div className="bg-[#0f2b34cc] shadow-md shadow-teal-700 p-4 rounded-lg text-center">
        <h3 className="text-gray-300 text-lg font-semibold">IPs</h3>
        <p className="text-teal-400 text-2xl md:text-5xl font-semibold">
          {counts.ips}
        </p>
      </div>
      
      <div className="bg-[#0f2b34cc] shadow-md shadow-teal-700 p-4 rounded-lg text-center">
        <h3 className="text-gray-300 text-lg font-semibold">Domains</h3>
        <p className="text-teal-400 text-2xl md:text-5xl font-semibold">
          {counts.domains}
        </p>
      </div>
      
      <div className="col-span-2 md:col-span-1 bg-[#0f2b34cc] shadow-md shadow-teal-700 p-4 rounded-lg text-center">
        <h3 className="text-gray-300 text-lg font-semibold">Credit Cards</h3>
        <p className="text-teal-400 text-2xl md:text-5xl font-semibold">
          {counts.creditCards}
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
