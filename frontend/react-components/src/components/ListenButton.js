import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from "react-bootstrap";
import styles from "./ListenButton.module.css";
const ListenButton = () => {
  return (
    <Button className={styles.listenButton} variant="primary">
      Listen To Your Daily Run Down
    </Button>
  );
};

export default ListenButton;
