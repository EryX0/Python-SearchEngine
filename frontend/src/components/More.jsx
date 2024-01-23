import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  Typography,
  Button,
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
            <Typography className="text-white text-justify">
              {item.article}
            </Typography>
          </DialogContentText>
        <DialogActions>
          <Button
            style={{ margin: "20px 0" }}
            fullWidth
            color="secondary"
            variant="outlined"
            onClick={() => setOpen(false)}
          >
            Close
          </Button>
        </DialogActions>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default More;
