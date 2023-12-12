import styles from "./NewsSection.module.css";
const NewsSection = () => {
  return (
    <div className={styles.newsSection}>
      <h4 className={styles.sectionHeader}>Business</h4>
      <h3 className={styles.stories}>
        <ul className={styles.deltaPassengersMissingDog}>
          <li className={styles.deltaPassengersMissing}>
            Delta passenger's missing dog found safe after 3 weeks
          </li>
          <li className={styles.deltaPassengersMissing}>
            Energy Secretary's EV Charger Hunt Hits Roadblock
          </li>
          <li>Supply concerns push oil prices to 9-month high.</li>
        </ul>
      </h3>
    </div>
  );
};

export default NewsSection;
