const Main = ({searchVal, setSearchVal, handleKeyDown}) => {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center">
      <input type="text" placeholder="Enter URL" onKeyDown={handleKeyDown} spellCheck={false} 
        value={searchVal} onChange={e=>setSearchVal(e.target.value)}
        className="w-[40%] px-4 py-2 text-lg text-white bg-transparent rounded-md outline outline-teal-500
            focus:outline-gray-300  transition-all duration-200 placeholder-gray-400"
      />
    </div>
  );
};

export default Main;
