import { LinearProgress } from "@mui/material";

const Loading = () => {
  return (
    <div className="animate-pulse w-4/5 mx-auto">
      <h1 className="text-center text-2xl pt-8 font-bold sm:text-4xl">
        Loading...
      </h1>
      <LinearProgress
        className="w-4/5 mx-auto mt-3 sm:w-1/2"
        color="secondary"
      />
    </div>
  );
};

export default Loading;
