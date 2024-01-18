import {
  Dialog,
  DialogContent,
  DialogContentText,
  Typography,
} from "@mui/material";
import "../more.css";

const More = ({ open, setOpen, item }) => {
  return (
    <div id="more">
      <Dialog
        open={open}
        onClose={() => setOpen(false)}
        sx={{ backdropFilter: "blur(3px)" }}
      >
        <DialogContent
          sx={{ background: "#100c23", border: "3px solid #EC83BB" }}
        >
          <DialogContentText>
            <Typography className="text-white text-justify">{item.article}</Typography>
          </DialogContentText>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default More;
