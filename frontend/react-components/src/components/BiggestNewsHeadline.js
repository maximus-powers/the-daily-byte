import styles from "./BiggestNewsHeadline.module.css";
const BiggestNewsHeadline = () => {
  return (
    <div className={styles.biggestNewsHeadline}>
      <h2 className={styles.newsHeadlineBased}>
        NEWS HEADLINE BASED ON SETTINGS
      </h2>
      <p
        className={styles.oneSentenceSummary}
      >{`One sentence summary of the most important article `}</p>
    </div>
  );
};

export default BiggestNewsHeadline;
