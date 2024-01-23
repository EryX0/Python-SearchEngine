import { useState } from "react";
import Loading from "./Loading";
import ShowContent from "./ShowContent";
import More from "./More";

const Content = ({ data, loading, score }) => {
  const [item, setItem] = useState(0);
  const [open, setOpen] = useState(false);

  return (
    <div className="text-white my-10">
      {data && (
        <>
          {data.length > 0 ? (
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-1">
              {score === "tf_idf" ? (
                <>
                  {[...data]
                    .sort((a, b) => b.tfidf_score - a.tfidf_score)
                    .map((i) => (
                      <ShowContent
                        key={i.document_number}
                        item={i}
                        tfidf={true}
                        setOpen={setOpen}
                        setItem={setItem}
                      />
                    ))}
                </>
              ) : (
                <>
                  {[...data]
                    .sort((a, b) => b.vsm_score - a.vsm_score)
                    .map((i) => (
                      <ShowContent
                        key={i.document_number}
                        item={i}
                        tfidf={false}
                        setOpen={setOpen}
                        setItem={setItem}
                      />
                    ))}
                </>
              )}
            </div>
          ) : (
            <div>
              <h1 className="text-center text-2xl pt-8 font-bold sm:text-4xl">
                Sorry! We did not find any results!
              </h1>
            </div>
          )}
        </>
      )}

      {loading && <Loading />}

      <More open={open} setOpen={setOpen} item={item} />
    </div>
  );
};

export default Content;
