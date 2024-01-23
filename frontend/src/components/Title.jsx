const Title = ({ data }) => {
  return (
    <div
      className={`${
        data && `opacity-0 text-xs sm:text-xs`
      } transition-all duration-500 text-3xl text-white text-center pt-14 font-bold sm:text-6xl`}
    >
      <h1>
        Search with <span className="text-pink_title">Seamless</span> Power
      </h1>
    </div>
  );
};

export default Title;
