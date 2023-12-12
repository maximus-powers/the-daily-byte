import "bootstrap/dist/css/bootstrap.min.css";
import { h6 } from "react-bootstrap";
import styles from "./HeaderAboveLogo.module.css";
const HeaderAboveLogo = () => {
  return (
    <section className={styles.headerAboveLogo}>
      <h6 className={styles.aiPoweredNews} />
      <h6 className={styles.aiPoweredNews} />
    </section>
  );
};

export default HeaderAboveLogo;
