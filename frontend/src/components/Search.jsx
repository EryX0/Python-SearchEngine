import { useState } from "react";
import axios from "axios";
import { FaSearch, FaArrowAltCircleRight } from "react-icons/fa";

const Search = ({ setData, data, setLoading }) => {
  const [value, setValue] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (value === "") {
      alert("Enter Somthing");
      return;
    }

    try {
      setData(null);
      setLoading(true);
      const { data } = await axios.get(
        `http://185.81.97.49:5000/search?query=${value}`,
        { headers: { "Content-Type": "application/json" } }
      );

      setData(data);
      console.log(data);
    } catch (err) {
      console.log(err);
      alert("Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`${
        data ? "pt-0 -translate-y-4" : "pt-24"
      } w-4/5 mx-auto transition-all duraition-500 sm:w-1/2 sm:${
        data ? "pt-0 sm:-translate-y-4" : "pt-28"
      }`}
    >
      <form
        onSubmit={handleSubmit}
        className="flex flex-col justify-center items-center relative"
      >
        <input
          type="text"
          className="bg-input_bg w-full p-4 text-white transition-all duration-200 rounded-lg outline-none outline-input_border sm:px-14 focus:shadow-2xl focus:shadow-input_shadow"
          placeholder="Ask a question"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
        <FaSearch className="hidden text-white left-3 top-[15px] text-2xl sm:block sm:absolute" />
        <button type="submit">
          <FaArrowAltCircleRight className="absolute text-white right-3 top-[15px] text-2xl transition-all duration-200 sm:block sm:absolute hover:scale-90" />
        </button>
      </form>
    </div>
  );
};

export default Search;
