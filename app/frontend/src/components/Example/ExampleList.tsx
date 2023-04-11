import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    {
        text: "正常DMS计算公式是什么?",
        value: "正常DMS计算公式是什么?"
    },
    { text: "进货未销定义是什么?", value: "进货未销定义?" },
    { text: "APP与OSPC端门店货源查询退货状态不一致 门店商品退货状态系统逻辑?", value: "APP与OSPC端门店货源查询退货状态不一致 门店商品退货状态系统逻辑?" }
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
