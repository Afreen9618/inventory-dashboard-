"use client";

import { useState } from "react";
import Papa from "papaparse";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function InventoryCleaner() {
  const [csvData, setCsvData] = useState([]);
  const [fileName, setFileName] = useState("");
  const [dailyChart, setDailyChart] = useState([]);
  const [weeklyChart, setWeeklyChart] = useState([]);
  const [monthlyChart, setMonthlyChart] = useState([]);

  const handleFileUpload = (file: any) => {
    setFileName(file.name);

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (result: any) => {
        const rows = result.data;
        setCsvData(rows);
        processCharts(rows);
      },
    });
  };

  const onDrop = (e: any) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    handleFileUpload(file);
  };

  const processCharts = (rows: any[]) => {
    const daily: any = {};
    const weekly: any = {};
    const monthly: any = {};

    rows.forEach((row: any) => {
      const date = new Date(row["Date"]);
      if (!date) return;

      const day = date.toISOString().split("T")[0];
      const week = `Week-${Math.ceil(date.getDate() / 7)}`;
      const month = date.toLocaleString("default", { month: "short" });

      daily[day] = (daily[day] || 0) + 1;
      weekly[week] = (weekly[week] || 0) + 1;
      monthly[month] = (monthly[month] || 0) + 1;
    });

    setDailyChart(formatChart(daily));
    setWeeklyChart(formatChart(weekly));
    setMonthlyChart(formatChart(monthly));
  };

  const formatChart = (obj: any) =>
    Object.keys(obj).map((key) => ({ label: key, value: obj[key] }));

  return (
    <div className="min-h-screen bg-[#0E1117] text-white p-10">

      {/* TITLE */}
      <h1 className="text-5xl font-bold mb-10 text-center">
        Inventory Cleaner Dashboard
      </h1>

      {/* UPLOAD BOX */}
      <div
        className="border-2 border-dashed border-gray-600 bg-[#1A1F29] p-10 rounded-xl text-center cursor-pointer hover:bg-[#222833] transition"
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
      >
        <div className="text-6xl mb-3">📤</div>
        <p className="text-xl">Drag & Drop your CSV file here</p>
        <p className="text-gray-400">Max 200MB • Only CSV files allowed</p>

        <input
          type="file"
          accept=".csv"
          className="hidden"
          id="fileInput"
          onChange={(e) => handleFileUpload(e.target.files![0])}
        />

        <label
          htmlFor="fileInput"
          className="mt-4 inline-block bg-blue-600 px-6 py-3 rounded-lg hover:bg-blue-700 transition cursor-pointer"
        >
          Browse Files
        </label>
      </div>

      {/* FILE STATUS */}
      {!fileName ? (
        <p className="mt-5 text-center text-blue-300">
          Upload a CSV file to continue.
        </p>
      ) : (
        <p className="mt-5 text-center text-green-400 text-xl">
          ✔ Uploaded: {fileName}
        </p>
      )}

      {/* PREVIEW TABLE */}
      {csvData.length > 0 && (
        <div className="mt-10 bg-[#1A1F29] p-6 rounded-xl overflow-auto">
          <h2 className="text-2xl mb-4 font-semibold">Preview Data</h2>
          <table className="table-auto w-full border border-gray-700 text-left">
            <thead>
              <tr>
                {Object.keys(csvData[0]).map((key, i) => (
                  <th key={i} className="border p-2 bg-[#222833]">
                    {key}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {csvData.slice(0, 10).map((row, i) => (
                <tr key={i}>
                  {Object.values(row).map((val: any, j) => (
                    <td key={j} className="border p-2">
                      {val}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          <p className="text-gray-400 mt-2">Showing first 10 rows only…</p>
        </div>
      )}

      {/* CHARTS */}
      {csvData.length > 0 && (
        <div className="mt-10">
          <h2 className="text-3xl mb-6 font-semibold text-center">
            Inventory Charts
          </h2>

          {/* DAILY */}
          <ChartBlock title="Daily Activity" data={dailyChart} />

          {/* WEEKLY */}
          <ChartBlock title="Weekly Activity" data={weeklyChart} />

          {/* MONTHLY */}
          <ChartBlock title="Monthly Activity" data={monthlyChart} />
        </div>
      )}
    </div>
  );
}

function ChartBlock({ title, data }: any) {
  return (
    <div className="bg-[#1A1F29] p-6 mb-10 rounded-xl">
      <h3 className="text-xl mb-4 font-semibold">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}














