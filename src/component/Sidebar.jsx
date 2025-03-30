import React, { useEffect, useState } from "react";
import { FaDeleteLeft } from "react-icons/fa6";
import { GoSidebarCollapse, GoSidebarExpand } from "react-icons/go";

const Sidebar = ({showSidebar, setShowSidebar, setSearchVal, refresh}) => {
    const [searchList, setSearchList] = useState([])
    const [hoveredIndex, setHoveredIndex] = useState(null);
    
    useEffect(()=>{
        localStorage.removeItem("searchHistory");
    },[])
    
    useEffect(()=>{
        let storedSearches = JSON.parse(localStorage.getItem("searchHistory")) || [];
        if(storedSearches){
            setSearchList(storedSearches)
        }
    },[refresh])

    const deleteSearch = (index) => {
       // Get current search history from localStorage
      let storedSearches = JSON.parse(localStorage.getItem("searchHistory")) || [];

      // Filter out the deleted item
      storedSearches = storedSearches.filter((_, i) => i !== index);

      // Update localStorage
      localStorage.setItem("searchHistory", JSON.stringify(storedSearches));

      // Update state
      setSearchList(storedSearches);
    }

  return (
    <>
      <div
        className={`h-full bg-[#0f2b34] border-l border-teal-500 md:border-none z-50 absolute top-0 right-0 transition-all duration-300 overflow-hidden ${
          showSidebar ? "w-[90vw] md:w-2/12 opacity-1" : "w-0 md:opacity-0"
        }`}>
        <p className="p-2 md:p-3 text-sm font-semibold text-teal-500 text-nowrap overflow-hidden">Recent Searches</p>

        <div className="p-2 md:p-3 w-full h-auto mt-4 md:mt-2 flex flex-col-reverse gap-2 text-sm text-teal-500 overflow-hidden">
            {searchList?.map((item, i)=>(
                <div key={i} className="relative cursor-pointer" onMouseEnter={() => setHoveredIndex(i)}
                    onMouseLeave={() => setHoveredIndex(null)} onClick={()=>setSearchVal(item)}>
                    <p className="text-nowrap overflow-hidden text-ellipsis p-1 bg-teal-900 rounded-md z-10">
                        {item}
                    </p>

                    <div className={`px-2 bg-teal-900 z-20 absolute top-1 right-0 transition-all duration-200
                        ${hoveredIndex === i ? 'opacity-1': 'opacity-0'}`}>
                        <FaDeleteLeft className="text-lg text-teal-600 cursor-pointer"
                            onClick={(e)=>{
                              e.stopPropagation();
                              deleteSearch(i);
                            }}/>
                    </div>
                </div>
            ))}
        </div>

      </div>

      {showSidebar ? (
        <GoSidebarCollapse
          className="z-50 absolute top-2 md:top-3 right-2 md:right-3 text-2xl text-teal-500 cursor-pointer"
          onClick={() => setShowSidebar(false)}
        />
      ) : (
        <GoSidebarExpand
          className="z-50 absolute top-2 md:top-3 right-2 md:right-3 text-2xl text-teal-500 cursor-pointer"
          onClick={() => setShowSidebar(true)}
        />
      )}
    </>
  );
};

export default Sidebar;
