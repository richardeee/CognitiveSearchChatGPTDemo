import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    {
        text: "迈瑞医疗2022年主要会计数据和财务指标?",
        value: "迈瑞医疗2022年上半年主要会计数据和财务指标?"
    },
    { text: "迈瑞医疗发行人基本情况?", value: "迈瑞医疗发行人基本情况?" },
    { text: "迈瑞医疗审计报告中的应收账款表", value: "迈瑞医疗审计报告中的应收账款表" }
];

interface Props {
    onExampleClicked: (value: string) => void;
}

export const ExampleList = ({ onExampleClicked }: Props) => {
    return (
        <ul className={styles.examplesNavList}>
            {EXAMPLES.map((x, i) => (
                <li key={i}>
                    <Example text={x.text} value={x.value} onClick={onExampleClicked} />
                </li>
            ))}
        </ul>
    );
};
