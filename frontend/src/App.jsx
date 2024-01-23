
import { useEffect, useState } from "react";

import { FaArrowCircleUp } from "react-icons/fa";
import Search from "./components/Search";
import Title from "./components/Title";
import Content from "./components/Content";
import Sort from "./components/Sort";

const App = () => {
  const [data, setData] = useState(null);
  const [score, setScore] = useState("tf_idf");
  const [scroll, setScroll] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleScroll = () => {
    setScroll(window.scrollY);
  };

  useEffect(() => {
    window.addEventListener("scroll", handleScroll);

    return () => window.removeEventListener("scroll", handleScroll);
  }, [window.scrollY]);

  return (
    <div style={{ minHeight: "100vh" }}>
      <div className="w-[90%] mx-auto">
        <Title data={data} />
        <Search data={data} setData={setData} setLoading={setLoading} />
        {data && data.length > 0 && <Sort score={score} setScore={setScore} />}

        <Content data={data} score={score} loading={loading} />

        {data && data.length > 0 && scroll > 700 && (

          <a
            href="#"
            className="text-right sticky float-right bottom-8 transition-all duration-300 hover:scale-90"
          >
            <FaArrowCircleUp className="cursor-pointer text-pink_title text-2xl sm:text-3xl" />
          </a>
        )}
      </div>
    </div>
  );
};

export default App;
