import { parseSupportingContentItem } from "./SupportingContentParser";

import styles from "./SupportingContent.module.css";

interface Props {
    supportingContent: string;
}

export const SupportingContent = ({ supportingContent }: Props) => {
    console.log('supportingContent' + supportingContent)
    const supportingContentList = eval(supportingContent)
    console.log('supportingContentList' + supportingContentList)
    return (
        <ul className={styles.supportingContentNavList}>
            {supportingContentList.map((x, i) => {
                const parsed = parseSupportingContentItem(x);

                return (
                    <li className={styles.supportingContentItem} key={i}>
                        <h4 className={styles.supportingContentItemHeader}>{parsed.title}</h4>
                        <p className={styles.supportingContentItemText}>{parsed.content}</p>
                        <a className={styles.supportingContentItemText} href={parsed.url} target="_blank">{parsed.url}</a>
                    </li>
                );
            })}
        </ul>
    );
};
