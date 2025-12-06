import React, { useState } from "react";
import Papa from "papaparse";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function InventoryCleaner() {
  const [csvData, setCsvData] = useState([]);
  const [totalCartons, setTotalCartons] = useState(0);
  const [fclNo, setFclNo] = useState("");

  const [dailyData, setDailyData] = useState([]);
  const [weeklyData, setWeeklyData] = useState([]);
  const [monthlyData, setMonthlyData] = useState([]);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (result) => {
        const data = result.data;

        // TOTAL CARTONS
        const cartonsTotal = data.reduce((sum, row) => {
          const value = parseInt(row["No of Cartons"]) || 0;
          return sum + value;
        }, 0);

        setCsvData(data);
        setTotalCartons(cartonsTotal);

        generateCharts(data);
      },
    });
  };

  // -------------------------------------------------------------
  // GENERATE DAILY, WEEKLY, MONTHLY CHART STRUCTURE
  // -------------------------------------------------------------
  const generateCharts = (data) => {
    const dailyMap = {};
    const weeklyMap = {};
    const monthlyMap = {};

    data.forEach((row) => {
      const dateStr = row["Date"];
      const cartons = parseInt(row["No of Cartons"]) || 0;

      if (!dateStr) return;

      const date = new Date(dateStr);

      // DAILY
      const dayKey = date.toISOString().split("T")[0];
      dailyMap[dayKey] = (dailyMap[dayKey] || 0) + cartons;

      // WEEKLY (ISO WEEK)
      const weekKey =
        date.getFullYear() + "-W" + getWeekNumber(date);
      weeklyMap[weekKey] = (weeklyMap[weekKey] || 0) + cartons;

      // MONTHLY
      const monthKey =
        date.getFullYear() + "-" + String(date.getMonth() + 1).padStart(2, "0");
      monthlyMap[monthKey] = (monthlyMap[monthKey] || 0) + cartons;
    });

    setDailyData(
      Object.keys(dailyMap).map((key) => ({
        date: key,
        cartons: dailyMap[key],
      }))
    );

    setWeeklyData(
      Object.keys(weeklyMap).map((key) => ({
        week: key,
        cartons: weeklyMap[key],
      }))
    );

    setMonthlyData(
      Object.keys(monthlyMap).map((key) => ({
        month: key,
        cartons: monthlyMap[key],
      }))
    );
  };

  // -------------------------------------------------------------
  // FUNCTION: GET WEEK NUMBER
  // -------------------------------------------------------------
  function getWeekNumber(date) {
    const firstDay = new Date(date.getFullYear(), 0, 1);
    const days = Math.floor(
      (date - firstDay) / (24 * 60 * 60 * 1000)
    );
    return Math.ceil((days + firstDay.getDay() + 1) / 7);
  }

  return (
    <div className="p-6 text-white bg-gray-900 min-h-screen">
      <h1 className="text-4xl font-bold mb-6">Inventory Cleaner</h1>

      {/* FCL NO */}
      <div className="mb-6">
        <label className="block font-semibold mb-2">FCL No.</label>
        <input
          type="text"
          className="p-3 w-80 rounded bg-gray-800 border border-gray-700"
          placeholder="Enter FCL Number"
          value={fclNo}
          onChange={(e) => setFclNo(e.target.value)}
        />
      </div>

      {/* FILE UPLOAD */}
      <div className="mb-6">
        <label className="block font-semibold mb-2">Upload CSV File</label>
        <input
          type="file"
          accept=".csv"
          className="p-3 rounded bg-gray-800 border border-gray-700"
          onChange={handleFileUpload}
        />
      </div>

      {/* TOTAL CARTONS */}
      {csvData.length > 0 && (
        <div className="bg-blue-900 p-4 mb-4 rounded text-lg font-semibold">
          Total No. of Cartons:{" "}
          <span className="text-yellow-300">{totalCartons}</span>
        </div>
      )}

      {/* ---------------- DAILY BAR CHART ---------------- */}
      {dailyData.length > 0 && (
        <div className="bg-gray-800 p-4 rounded mb-6">
          <h2 className="text-xl mb-3 font-semibold">Daily Cartons Chart</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={dailyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="cartons" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* ---------------- WEEKLY BAR CHART ---------------- */}
      {weeklyData.length > 0 && (
        <div className="bg-gray-800 p-4 rounded mb-6">
          <h2 className="text-xl mb-3 font-semibold">Weekly Cartons Chart</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="cartons" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* ---------------- MONTHLY BAR CHART ---------------- */}
      {monthlyData.length > 0 && (
        <div className="bg-gray-800 p-4 rounded mb-6">
          <h2 className="text-xl mb-3 font-semibold">Monthly Cartons Chart</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="cartons" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}












