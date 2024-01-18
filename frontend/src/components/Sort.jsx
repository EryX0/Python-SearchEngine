import { FaSortAmountDown } from "react-icons/fa";

const Sort = ({ setScore }) => {
  // ml-[4.3rem] sm:ml-[34rem]
  return (
    <div className="flex w-[300px] mx-auto text-white my-10">
      <div className="w-full mx-auto flex">
        <p className="flex justify-evenly items-center w-1/2 p-5 rounded-l-full border border-input_border border-2 border-r-[1px] bg-bg_select border-r-gray-300">
          <FaSortAmountDown /> Sort by
        </p>

        <select
          className="w-1/2 p-5 pl-12 rounded-r-full border border-input_border border-2 border-l-0 bg-bg_select focus:outline-none"
          onChange={(e) => setScore(e.currentTarget.value)}
        >
          <option value="tf_idf" defaultValue>
            TF-IDF
          </option>
          <option value="vsm">VSM</option>
        </select>
      </div>
    </div>
  );
};

export default Sort;
