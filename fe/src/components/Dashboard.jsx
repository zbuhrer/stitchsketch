import React, { useState, useEffect } from "react";

function Dashboard({ authAxios, onLogout }) {
  const [opportunities, setOpportunities] = useState([]);
  const [mediaItems, setMediaItems] = useState({});

  useEffect(() => {
    const fetchOpportunities = async () => {
      try {
        const response = await authAxios.get("/Opportunities");
        setOpportunities(response.data);
        // Fetch associated media for each opportunity
        response.data.forEach((opp) => {
          fetchMediaForOpportunity(opp.id);
        });
      } catch (err) {
        console.error("Failed to fetch opportunities:", err);
      }
    };

    fetchOpportunities();
  }, [authAxios]);

  const fetchMediaForOpportunity = async (oppId) => {
    try {
      const response = await authAxios.get(`/Opportunities/${oppId}/media`);
      setMediaItems((prev) => ({
        ...prev,
        [oppId]: response.data,
      }));
    } catch (err) {
      console.error(`Failed to fetch media for opportunity ${oppId}:`, err);
    }
  };

  return (
    <div className="dashboard-container">
      <h2>Opportunities Media Dashboard</h2>
      {opportunities.map((opp) => (
        <div key={opp.id} className="opportunity-card">
          <h3>{opp.name}</h3>
          <div className="media-grid">
            {mediaItems[opp.id]?.map((item) => (
              <MediaDisplay key={item.id} item={item} />
            ))}
          </div>
        </div>
      ))}
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default Dashboard;
