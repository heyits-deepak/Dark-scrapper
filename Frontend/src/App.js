import { useEffect, useState } from "react";
import Sidebar from "./component/Sidebar";
import Main from "./component/Main";
import data from './utils/demoData.json'

function App() {
  const [showSidebar, setShowSidebar] = useState(false)
  const [searchVal, setSearchVal] = useState('')
  const [refresh, setRefresh] = useState(0)
  const [moveInput, setMoveInput] = useState(false)

  useEffect(()=>{
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
  };
  },[])

  
useEffect(() => {
  setMoveInput(false); // Reset moveInput when searchVal changes
}, [searchVal]);

  const executeSearch = (inputUrl) =>{

  }

  const handleKeyDown = (event) => {

    if (event.ctrlKey && (event.key === "+" || event.key === "-" || event.key === "=")) {
        event.preventDefault();
    }

    if (event.key === "Enter" && searchVal.trim() !== ""){ 
      let storedSearches = JSON.parse(localStorage.getItem("searchHistory")) || [];

      // Remove existing instance of searchVal if it exists
  storedSearches = storedSearches.filter((item) => item.trim() !== searchVal.trim());

  // Add the new search value
  storedSearches.push(searchVal);

  // Update localStorage
  localStorage.setItem("searchHistory", JSON.stringify(storedSearches));

      setRefresh(prev=>prev+1)
      executeSearch(searchVal)
      setMoveInput(true)
    } 
};

  return (
    <div className="App h-auto md:h-screen backdrop-blur-sm flex justify-between border border-teal-500 md:border-none">

      <a href="https://www.linkedin.com/in/deepak-sharma-4b2032240/" target="_blank" 
        className="absolute top-2 md:top-2 left-2 md:left-2 flex flex-col cursor-pointer z-40">
        <span className="text-2xl font-semibold text-teal-500 uppercase">Dark Scrapper</span>
        <span className="hidden md:block text-xs text-cyan-500 text-nowrap uppercase">By Deepak Sharma</span>
      </a>
      
      <div className={`h-full  transition-all duration-300 ${showSidebar ? 'z-10 w-[100vw] md:w-10/12':'w-[100vw]'}`}>
        <Main searchVal={searchVal} setSearchVal={setSearchVal} handleKeyDown={handleKeyDown}
        moveInput={moveInput} data={data}/>
      </div>

      <Sidebar showSidebar={showSidebar} setShowSidebar={setShowSidebar} setSearchVal={setSearchVal}
        moveInput={moveInput} refresh={refresh} />
    </div>
  );
}

export default App;
