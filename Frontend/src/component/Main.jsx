import Dashboard from "./Dashboard";
import Visualization from "./Visualization";

const Main = ({searchVal, setSearchVal, handleKeyDown, moveInput, data, refresh}) => {

  return (
    <div className="w-full h-full flex flex-col items-center justify-center">
    
      <input type="text" placeholder="Enter URL" onKeyDown={handleKeyDown} spellCheck={false} 
        value={searchVal} onChange={e=>setSearchVal(e.target.value)}
        className={`w-[90%] md:w-[40%] z-50 px-4 py-2 text-lg text-white bg-transparent rounded-md outline outline-teal-500 
          focus:outline-gray-300  transition-all duration-500 placeholder-gray-400 input-transition ${moveInput ? "move-up" : "move-down"} `}
      />

      <div className="z-40 w-full h-full flex flex-col justify-center items-center p-2 mb-[2vh] mt-[10vh] md:my-0 md:mt-[3vh] overflow-hidden">
        <Dashboard data={data} moveInput={moveInput}/>
        <Visualization data={data} moveInput={moveInput}/>
      </div>
    </div>
  );
};

export default Main;
