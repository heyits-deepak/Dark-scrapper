import { useEffect, useState } from "react";
import Sidebar from "./component/Sidebar";
import Main from "./component/Main";
import  dummyData from "./utils/demoData.json"
function App() {
  const [showSidebar, setShowSidebar] = useState(false);
  const [searchVal, setSearchVal] = useState("");
  const [refresh, setRefresh] = useState(0);
  const [moveInput, setMoveInput] = useState(false);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  useEffect(() => {
    setMoveInput(false);
  }, [searchVal]);

  const executeSearch = async (inputUrl) => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ link: inputUrl }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      console.log("API result:", result);

      // Ensure summary is present and valid
      if (!result || typeof result !== "object" || !result.summary) {
        throw new Error("Invalid response: Missing or malformed 'summary' field");
      }

      setData(result);
    } catch (err) {
      console.error("Fetch error:", err);
      setError(err.message || "Something went wrong while fetching data.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    // Disable zoom in/out using Ctrl + +/-/=
    if (event.ctrlKey && (event.key === "+" || event.key === "-" || event.key === "=")) {
      event.preventDefault();
    }

    if (event.key === "Enter" && searchVal.trim() !== "") {
      // Save to localStorage
      let storedSearches = JSON.parse(localStorage.getItem("searchHistory")) || [];

      // Prevent duplicates
      storedSearches = storedSearches.filter((item) => item.trim() !== searchVal.trim());
      storedSearches.push(searchVal.trim());
      localStorage.setItem("searchHistory", JSON.stringify(storedSearches));

      // Trigger data fetch
      setRefresh((prev) => prev + 1);
      executeSearch(searchVal.trim());
      setMoveInput(true);
    }
  };

  return (
    <div className="App h-auto md:h-screen backdrop-blur-sm flex justify-between border border-teal-500 md:border-none">
      <a
        href="https://www.linkedin.com/in/deepak-sharma-4b2032240/"
        target="_blank"
        rel="noreferrer"
        className="absolute top-2 md:top-2 left-2 md:left-2 flex flex-col cursor-pointer z-40"
      >
        <span className="text-2xl font-semibold text-teal-500 uppercase">Dark Scrapper</span>
        <span className="hidden md:block text-xs text-cyan-500 text-nowrap uppercase">By Deepak Sharma</span>
      </a>

      <div className={`h-full transition-all duration-300 ${showSidebar ? "z-10 w-[100vw] md:w-10/12" : "w-[100vw]"}`}>
        <Main
          searchVal={searchVal}
          setSearchVal={setSearchVal}
          handleKeyDown={handleKeyDown}
          moveInput={moveInput}
          data={dummyData}
          loading={loading}
          error={error}
        />
      </div>

      <Sidebar
        showSidebar={showSidebar}
        setShowSidebar={setShowSidebar}
        setSearchVal={setSearchVal}
        moveInput={moveInput}
        refresh={refresh}
      />
    </div>
  );
}

export default App;