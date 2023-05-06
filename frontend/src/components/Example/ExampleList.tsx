import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    {
        text: "科大讯飞2022年上半年主要会计数据和财务指标?",
        value: "科大讯飞2022年上半年主要会计数据和财务指标?"
    },
    { text: "南京江宁科学园发展有限公司发行人基本情况?", value: "南京江宁科学园发展有限公司发行人基本情况?" },
    { text: "南京江宁科学园发展有限公司审计报告中的应收账款表", value: "南京江宁科学园发展有限公司审计报告中的应收账款表" }
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
