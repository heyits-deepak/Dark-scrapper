import { useEffect, useState } from "react";
import Sidebar from "./component/Sidebar";
import Main from "./component/Main";

function App() {
  const [showSidebar, setShowSidebar] = useState(false)
  const [searchVal, setSearchVal] = useState('')
  const [refresh, setRefresh] = useState(0)

  useEffect(()=>{
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
  };
  },[])

  const executeSearch = (inputUrl) =>{

  }

  const handleKeyDown = (event) => {

    if (event.ctrlKey && (event.key === "+" || event.key === "-" || event.key === "=")) {
        event.preventDefault();
    }

    if (event.key === "Enter" && searchVal.trim() !== ""){ 
      let storedSearches = JSON.parse(localStorage.getItem("searchHistory")) || [];

      storedSearches.push(searchVal);  // Add new search value
      localStorage.setItem("searchHistory", JSON.stringify(storedSearches));

      setRefresh(prev=>prev+1)
      executeSearch(searchVal)
    } 
};

  return (
    <div className="App backdrop-blur-sm flex justify-between">
      <div className={`h-full  transition-all duration-300 ${showSidebar ? 'w-10/12':'w-[100vw]'}`}>
        <Main searchVal={searchVal} setSearchVal={setSearchVal} handleKeyDown={handleKeyDown}/>
      </div>
      <Sidebar showSidebar={showSidebar} setShowSidebar={setShowSidebar} setSearchVal={setSearchVal} refresh={refresh} />
    </div>
  );
}

export default App;
