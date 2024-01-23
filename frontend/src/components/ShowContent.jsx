import { Button, Typography } from "@mui/material";

const ShowContent = ({ item, tfidf, setOpen, setItem }) => {
  return (
    <div
      className="bg-bg_result text-white rounded-lg p-5 border border-input_shadow border-[4px] w-4/5 mx-auto sm:w-1/2"
      key={item.document_number}
    >
      <h1 className="text-doc_title font-bold text-2xl mb-3">
        <a href={item.link} target="_blank">
          {item.title}
        </a>
      </h1>

      <div className="items-center">
        <Typography className="text-white text-justify">{item.highlight}</Typography>
        <Button
          style={{ margin: "20px 0 10px" }}
          variant="contained"
          color="secondary"
          fullWidth
          onClick={() => {
            setItem(item);
            setOpen(true);
          }}
        >
          See More
        </Button>
      </div>

      <hr className="my-4" />

      <div className="flex justify-between mt-3">
        <p className={`${tfidf ? "text-pink_title" : "text-white"}`}>
          tfidf_score: {item.tfidf_score.toFixed(5)}
        </p>
        <p className={`${!tfidf ? "text-pink_title" : "text-white"} flex`}>
          vsm_score: {item.vsm_score.toFixed(5)}
        </p>
      </div>
    </div>
  );
};

export default ShowContent;
