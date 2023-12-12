import styles from "./DateBar.module.css";
const DateBar = () => {
  return (
    <section className={styles.dateBar}>
      <img className={styles.dateBarChild} alt="" src="/undefined.png" />
      <div className={styles.frame}>
        <h5 className={styles.vol1}>VOL. 1</h5>
        <h5 className={styles.mondayDecember21}>MONDAY, DECEMBER 21, 2023</h5>
        <h5 className={styles.h5}>$0.00</h5>
      </div>
      <img className={styles.dateBarChild} alt="" src="/undefined1.png" />
    </section>
  );
};

export default DateBar;
