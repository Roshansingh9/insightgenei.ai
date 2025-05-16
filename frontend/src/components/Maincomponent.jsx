import { useState } from "react";

export default function QueryInterface() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  
  const columnMappings = [
    {
      name: "State",
      description:
        "The Indian state where the vehicle is registered (e.g., Karnataka, Rajasthan, Madhya Pradesh).",
    },
    {
      name: "Avg Daily Distance (km)",
      description:
        "Average distance driven per day in kilometers (e.g., 68.84, 23.8).",
    },
    {
      name: "Brand",
      description:
        "The manufacturer or brand of the vehicle (e.g., Royal Enfield, Bajaj, KTM).",
    },
    {
      name: "Model",
      description:
        "Specific model name of the vehicle (e.g., Hunter 350, Dominar 400, 125 Duke).",
    },
    {
      name: "Price (INR)",
      description:
        "Original purchase price of the vehicle in Indian Rupees (e.g., 252816, 131100).",
    },
    {
      name: "Year of Manufacture",
      description:
        "The year the vehicle was manufactured (e.g., 2019, 2020, 2021).",
    },
    {
      name: "Engine Capacity (cc)",
      description:
        "Engine capacity in cubic centimeters (e.g., 672, 769, 216).",
    },
    {
      name: "Fuel Type",
      description:
        "Type of fuel used by the vehicle (e.g., Electric, Hybrid, Petrol).",
    },
    {
      name: "Mileage (km/l)",
      description:
        "Fuel efficiency measured in kilometers per liter (e.g., 78.41, 89.98).",
    },
    {
      name: "Owner Type",
      description:
        "Indicates the ownership count such as First Owner, Second Owner, Third Owner (e.g., Second, Third).",
    },
    {
      name: "Registration Year",
      description:
        "Year the vehicle was registered with the RTO (e.g., 2019, 2021, 2024).",
    },
    {
      name: "Insurance Status",
      description:
        "Current insurance status of the vehicle (e.g., Active, Not Available).",
    },
    {
      name: "Seller Type",
      description:
        "Indicates whether the seller is the first-hand, second-hand, or third-hand owner (e.g., Individual, Dealer).",
    },
    {
      name: "Resale Price (INR)",
      description:
        "Expected or actual resale value in Indian Rupees (e.g., 149934.18, 66960.3).",
    },
    {
      name: "City Tier",
      description:
        "Tier classification of the city where the vehicle is sold: Tier 1 (metro), Tier 2 (semi-urban), Tier 3 (rural/small towns).",
    },
  ];
  

  // Function to submit query to backend API - UPDATED to use GET request
  const handleSubmit = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      // Changed to GET request with query param named 'text' to match backend
      const response = await fetch(
        `https://insightgenei-ai.onrender.com/query?text=${encodeURIComponent(
          query
        )}`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setResponse(data);
    } catch (err) {
      setError(err.message || "Failed to fetch response");
      console.error("API Error:", err);
    } finally {
      setLoading(false);
    }
  };

  // Format currency values
  const formatCurrency = (value) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 2,
    }).format(value);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6">
      <div className="max-w-4xl mx-auto space-y-10">
        {/* PART 1: Query Input Section */}
        <section className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h1 className="text-3xl font-bold mb-4">Enter your query</h1>
          <textarea
            className="w-full h-32 bg-gray-700 border border-gray-600 rounded-md p-3 text-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
            placeholder="Type your query here... (e.g., 'Show me motorcycles in Maharashtra with resale price under 25000')"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="mt-4 px-6 py-3 bg-gradient-to-r from-teal-600 to-blue-600 rounded-md font-medium text-white hover:from-teal-500 hover:to-blue-500 transition-colors disabled:opacity-50"
          >
            {loading ? "Processing..." : "Submit"}
          </button>
        </section>

        {/* PART 2: Response Display Section */}
        <section className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-4">Response</h2>

          {loading && (
            <div className="flex justify-center items-center min-h-32">
              <div className="animate-pulse text-blue-400">
                Processing your query... (Note: The first query might take a bit
                longer as the server starts up)
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-900/30 border border-red-700 text-red-200 p-4 rounded-md">
              {error}
            </div>
          )}

          {!loading && !error && !response && (
            <div className="bg-gray-700 rounded-md p-4 min-h-32">
              <p className="text-gray-400">Response will appear here...</p>
            </div>
          )}

          {!loading && !error && response && (
            <div className="space-y-6">
              {/* Data Table */}
              {response.data && response.data.length > 0 && (
                <div className="overflow-x-auto">
                  <h3 className="text-xl font-semibold mb-2 text-teal-400">
                    Results
                  </h3>
                  <table className="w-full border-collapse bg-gray-700 rounded-md overflow-hidden">
                    <thead>
                      <tr className="bg-gray-800 text-left">
                        {Object.keys(response.data[0]).map((key, index) => (
                          <th
                            key={index}
                            className="p-3 font-medium text-blue-300"
                          >
                            {key
                              .replace(/_/g, " ")
                              .replace(/\b\w/g, (c) => c.toUpperCase())}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {response.data.map((item, rowIndex) => (
                        <tr key={rowIndex} className="border-t border-gray-600">
                          {Object.entries(item).map(
                            ([key, value], colIndex) => (
                              <td
                                key={`${rowIndex}-${colIndex}`}
                                className="p-3 text-gray-200"
                              >
                                {key.includes("price") || key.includes("_inr")
                                  ? formatCurrency(value)
                                  : value}
                              </td>
                            )
                          )}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {/* Summary */}
              {response.summary && (
                <div className="mt-6">
                  <h3 className="text-xl font-semibold mb-2 text-teal-400">
                    Summary
                  </h3>
                  <div className="bg-gray-700 border border-gray-600 rounded-md p-4">
                    <p className="text-gray-200 leading-relaxed">
                      {response.summary}
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

        {/* PART 3: Column Mapping Reference */}
        <section className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-2">Column Mapping Reference</h2>
          <p className="text-gray-400 text-sm mb-4">
            Use these field names in your queries to reference database columns
            or
          </p>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse bg-gray-700 rounded-md overflow-hidden">
              <thead>
                <tr className="bg-gray-800 text-left">
                  <th className="p-3 font-medium text-blue-300">Feild Name</th>
                  <th className="p-3 font-medium text-blue-300">
                    Field Description
                  </th>
                </tr>
              </thead>
              <tbody>
                {columnMappings.map((column, index) => (
                  <tr
                    key={index}
                    className="border-t border-gray-600 hover:bg-gray-600/50 transition-colors"
                  >
                    <td className="p-3 text-gray-200">{column.name}</td>
                    <td className="p-3 text-gray-400 font-mono text-sm">
                      {column.description}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
