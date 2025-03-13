import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Dashboard = ({ setAuth }) => {
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         const response = await axios.get("http://localhost:4000/dashboard", {
//           headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
//         });
//         setMessage(response.data.message);
//       } catch (error) {
//         console.error("Error fetching dashboard data:", error);
//         navigate("/login");
//       }
//     };

//     fetchData();
//   }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setAuth(false);
    navigate("/login");
  };

  return (
    <div className="p-4">
      <h2>Dashboard</h2>
      {/* <p>{message}</p> */}
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Dashboard;
